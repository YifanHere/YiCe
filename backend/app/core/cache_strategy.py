"""Cache strategy implementation for YiCe data services."""
from enum import Enum
from typing import Any, Dict, Optional, Callable
from functools import wraps
import hashlib
import inspect
import json
import logging
from .redis_client import RedisClient
from .exceptions import CacheError

logger = logging.getLogger(__name__)


class DataType(Enum):
    """Enum for different data types with corresponding TTL values."""
    KLINE = "kline"
    FUNDAMENTAL = "fundamental"
    MACRO = "macro"


class CacheStrategy:
    """Cache strategy class handling key generation and TTL management."""
    
    # TTL in seconds: K线=1小时, 基本面=24小时, 宏观=7天
    TTL_CONFIG = {
        DataType.KLINE: 3600,
        DataType.FUNDAMENTAL: 86400,
        DataType.MACRO: 604800
    }
    
    def __init__(self):
        """Initialize cache strategy with Redis client."""
        self.redis_client = RedisClient()
    
    @staticmethod
    def generate_key(
        provider: str,
        data_type: DataType,
        symbol: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate cache key in format: yice:data:{provider}:{data_type}:{symbol}:{params_hash}
        
        Args:
            provider: Data provider name (e.g., "tushare")
            data_type: Type of data (DataType enum)
            symbol: Stock or asset symbol
            params: Additional parameters for the query
            
        Returns:
            Generated cache key string
        """
        key_parts = ["yice", "data", provider, data_type.value]
        
        if symbol:
            key_parts.append(symbol)
        
        if params:
            # Convert datetime objects to ISO format strings for serialization
            serializable_params = {}
            for key, value in params.items():
                if hasattr(value, 'isoformat'):  # datetime/date objects
                    serializable_params[key] = value.isoformat()
                else:
                    serializable_params[key] = value
            # Sort params to ensure consistent hashing
            sorted_params = json.dumps(serializable_params, sort_keys=True)
            params_hash = hashlib.md5(sorted_params.encode()).hexdigest()[:8]
            key_parts.append(params_hash)
        
        return ":".join(key_parts)
    
    @classmethod
    def get_ttl(cls, data_type: DataType) -> int:
        """
        Get TTL value for a specific data type.
        
        Args:
            data_type: Type of data
            
        Returns:
            TTL in seconds
        """
        return cls.TTL_CONFIG.get(data_type, 3600)  # Default to 1 hour
    
    async def get(self, key: str) -> Any:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        try:
            return await self.redis_client.get(key)
        except CacheError as e:
            logger.warning(f"Cache get operation failed for key {key}: {e}", exc_info=True)
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        data_type: Optional[DataType] = None,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set value in cache with appropriate TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            data_type: Data type for TTL determination
            ttl: Explicit TTL in seconds (overrides data_type)
            
        Returns:
            True if successful
        """
        if ttl is None and data_type is not None:
            ttl = self.get_ttl(data_type)
        
        try:
            return await self.redis_client.set(key, value, ttl=ttl)
        except CacheError as e:
            logger.warning(f"Cache set operation failed for key {key}: {e}", exc_info=True)
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Delete value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted
        """
        try:
            return await self.redis_client.delete(key)
        except CacheError as e:
            logger.warning(f"Cache delete operation failed for key {key}: {e}", exc_info=True)
            return False


def cached(
    provider: str,
    data_type: DataType,
    symbol_param: str = "symbol",
    exclude_params: Optional[list] = None
):
    """
    Decorator to cache async function results.
    
    Args:
        provider: Data provider name
        data_type: Type of data
        symbol_param: Name of the parameter containing the symbol
        exclude_params: List of parameters to exclude from cache key
        
    Returns:
        Decorated function
    """
    exclude_params = exclude_params or []
    cache_strategy = CacheStrategy()
    
    def decorator(func: Callable):
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            import time
            start_time = time.perf_counter()
            logger = logging.getLogger(__name__)
            
            # Bind arguments to parameter names
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            all_args = bound_args.arguments
            
            # Extract symbol
            symbol = all_args.get(symbol_param)
            
            # Build params dict, excluding specified params
            params = {k: v for k, v in all_args.items() 
                     if k not in exclude_params and k != symbol_param and k != 'self'}
            
            # Generate cache key
            cache_key = CacheStrategy.generate_key(
                provider=provider,
                data_type=data_type,
                symbol=symbol,
                params=params
            )
            
            # Try to get from cache first
            cached_result = await cache_strategy.get(cache_key)
            if cached_result is not None:
                elapsed = time.perf_counter() - start_time
                logger.debug(f"Cache hit for key {cache_key}, elapsed {elapsed:.3f}s")
                return cached_result
            
            # Cache miss, call the original function
            logger.debug(f"Cache miss for key {cache_key}")
            result = await func(*args, **kwargs)
            
            # Store in cache
            await cache_strategy.set(cache_key, result, data_type=data_type)
            elapsed = time.perf_counter() - start_time
            logger.debug(f"Cached result for key {cache_key}, total elapsed {elapsed:.3f}s")
            
            return result
        return wrapper
    return decorator
