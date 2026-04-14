"""统一缓存接口，支持Redis和本地文件缓存自动降级"""
from typing import Any, Optional
from .redis_client import RedisClient
from .file_cache import file_cache


class Cache:
    """统一缓存类，自动在Redis和本地文件缓存之间降级"""
    
    def __init__(self):
        self.redis_client = RedisClient()
        self.file_cache = file_cache
        self._use_redis: Optional[bool] = None
    
    async def _check_redis_available(self) -> bool:
        """检查Redis是否可用"""
        if self._use_redis is not None:
            return self._use_redis
        
        try:
            # 尝试一个简单的Redis操作
            await self.redis_client.exists("__health_check__")
            self._use_redis = True
        except Exception:
            self._use_redis = False
        
        return self._use_redis
    
    async def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值
        
        Args:
            key: 缓存键
            
        Returns:
            缓存值，如果不存在则返回None
        """
        if await self._check_redis_available():
            value = await self.redis_client.get(key)
            if value is not None:
                return value
        
        # Redis不可用或未找到，尝试文件缓存
        return self.file_cache.get(key)
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒，仅Redis支持）
        """
        if await self._check_redis_available():
            await self.redis_client.set(key, value, ttl=ttl)
        
        # 同时写入文件缓存作为备份
        self.file_cache.set(key, value)
    
    async def delete(self, key: str) -> None:
        """
        删除缓存值
        
        Args:
            key: 缓存键
        """
        if await self._check_redis_available():
            await self.redis_client.delete(key)
        
        self.file_cache.delete(key)
    
    async def exists(self, key: str) -> bool:
        """
        检查缓存键是否存在
        
        Args:
            key: 缓存键
            
        Returns:
            True如果存在
        """
        if await self._check_redis_available():
            if await self.redis_client.exists(key):
                return True
        
        return self.file_cache.get(key) is not None


# 全局缓存实例
cache = Cache()
