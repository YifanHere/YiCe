"""本地文件缓存实现，作为Redis的备选方案"""
import pickle
import hashlib
from pathlib import Path
from typing import Any, Optional


class FileCache:
    """基于pickle的文件缓存类"""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        初始化文件缓存
        
        Args:
            cache_dir: 缓存目录路径，默认为当前目录下的.cache文件夹
        """
        if cache_dir is None:
            # 默认缓存目录：项目根目录/.cache
            self.cache_dir = Path(__file__).parent.parent.parent / ".cache"
        else:
            self.cache_dir = Path(cache_dir)
        
        # 确保缓存目录存在
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, key: str) -> Path:
        """
        根据键生成缓存文件路径
        
        Args:
            key: 缓存键
            
        Returns:
            缓存文件路径
        """
        # 使用MD5哈希键以避免文件名问题
        key_hash = hashlib.md5(key.encode("utf-8")).hexdigest()
        return self.cache_dir / f"{key_hash}.pkl"
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值
        
        Args:
            key: 缓存键
            
        Returns:
            缓存值，如果不存在则返回None
        """
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, "rb") as f:
                return pickle.load(f)
        except (pickle.UnpicklingError, IOError, EOFError):
            # 如果读取失败，删除损坏的缓存文件
            cache_path.unlink(missing_ok=True)
            return None
    
    def set(self, key: str, value: Any) -> None:
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, "wb") as f:
                pickle.dump(value, f)
        except (pickle.PicklingError, IOError):
            # 写入失败时忽略
            pass
    
    def delete(self, key: str) -> None:
        """
        删除缓存值
        
        Args:
            key: 缓存键
        """
        cache_path = self._get_cache_path(key)
        cache_path.unlink(missing_ok=True)
    
    def clear(self) -> None:
        """清空所有缓存"""
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink(missing_ok=True)


# 全局文件缓存实例
file_cache = FileCache()
