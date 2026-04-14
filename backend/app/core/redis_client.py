"""Redis client wrapper for caching operations."""
import logging
import pickle
from typing import Any, Optional
from redis import asyncio as aioredis
from .config import settings
from .exceptions import CacheError

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client wrapper providing basic caching operations."""
    
    _instance: Optional["RedisClient"] = None
    _redis: Optional[aioredis.Redis] = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one Redis client instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def _get_redis(self) -> aioredis.Redis:
        """Get or create Redis connection pool."""
        if self._redis is None:
            self._redis = await aioredis.from_url(
                f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
                password=settings.REDIS_PASSWORD or None,
                encoding="utf-8",
                decode_responses=False
            )
        return self._redis
    
    async def close(self):
        """Close Redis connection."""
        if self._redis is not None:
            await self._redis.close()
            self._redis = None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set a key-value pair in Redis with optional TTL.
        
        Args:
            key: Redis key
            value: Value to store (will be pickled)
            ttl: Time to live in seconds
            
        Returns:
            True if successful
        """
        redis = await self._get_redis()
        try:
            serialized = pickle.dumps(value)
            await redis.set(key, serialized, ex=ttl)
            return True
        except Exception as e:
            logger.error(f"Redis set operation failed for key {key}: {e}", exc_info=True)
            raise CacheError("set", str(e), e) from e
    
    async def get(self, key: str) -> Any:
        """
        Get a value from Redis by key.
        
        Args:
            key: Redis key
            
        Returns:
            Unpickled value or None if not found
        """
        redis = await self._get_redis()
        try:
            serialized = await redis.get(key)
            if serialized is None:
                return None
            return pickle.loads(serialized)
        except Exception as e:
            logger.error(f"Redis get operation failed for key {key}: {e}", exc_info=True)
            raise CacheError("get", str(e), e) from e
    
    async def delete(self, key: str) -> bool:
        """
        Delete a key from Redis.
        
        Args:
            key: Redis key
            
        Returns:
            True if key was deleted
        """
        redis = await self._get_redis()
        try:
            result = await redis.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"Redis delete operation failed for key {key}: {e}", exc_info=True)
            raise CacheError("delete", str(e), e) from e
    
    async def exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis.
        
        Args:
            key: Redis key
            
        Returns:
            True if key exists
        """
        redis = await self._get_redis()
        try:
            return await redis.exists(key) > 0
        except Exception as e:
            logger.error(f"Redis exists operation failed for key {key}: {e}", exc_info=True)
            raise CacheError("exists", str(e), e) from e
