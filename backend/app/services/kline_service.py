"""K线数据获取服务"""
import logging
from datetime import datetime
from typing import List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import asyncio
from ..core.providers.factory import DataSourceFactory
from ..models.data_models import KlineData
from ..core.cache_strategy import cached, DataType


logger = logging.getLogger(__name__)


class RateLimiter:
    """简单的速率限制器（基于Tushare频控要求：每分钟不超过200次）"""
    
    def __init__(self, max_calls: int = 200, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        """获取调用权限，超过限制则等待"""
        async with self.lock:
            now = datetime.now().timestamp()
            # 清理过期的调用记录
            self.calls = [call_time for call_time in self.calls if now - call_time < self.period]
            # 如果超过限制，等待
            if len(self.calls) >= self.max_calls:
                wait_time = self.period - (now - self.calls[0])
                if wait_time > 0:
                    logger.warning(
                        f"Rate limit exceeded. Waiting {wait_time:.2f} seconds. "
                        f"Max calls: {self.max_calls}, period: {self.period}s"
                    )
                    await asyncio.sleep(wait_time)
            # 记录这次调用
            self.calls.append(datetime.now().timestamp())


class KlineDataService:
    """K线数据服务类，封装日K、周K、月K数据获取"""
    
    def __init__(self):
        """初始化K线数据服务"""
        self.provider = DataSourceFactory.get_provider("tushare")
        if not self.provider:
            raise ValueError("Failed to initialize Tushare provider")
        self.rate_limiter = RateLimiter()
    
    @cached(provider="tushare", data_type=DataType.KLINE)
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError, Exception))
    )
    async def get_daily_kline(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[KlineData]:
        """
        获取日K线数据
        
        Args:
            symbol: 股票代码（如 "000001.SZ"）
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            KlineData对象列表
        """
        await self.rate_limiter.acquire()
        return await self.provider.get_kline(symbol, start_date, end_date, period="daily")
    
    @cached(provider="tushare", data_type=DataType.KLINE)
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError, Exception))
    )
    async def get_weekly_kline(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[KlineData]:
        """
        获取周K线数据
        
        Args:
            symbol: 股票代码（如 "000001.SZ"）
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            KlineData对象列表
        """
        await self.rate_limiter.acquire()
        return await self.provider.get_kline(symbol, start_date, end_date, period="weekly")
    
    @cached(provider="tushare", data_type=DataType.KLINE)
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError, Exception))
    )
    async def get_monthly_kline(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[KlineData]:
        """
        获取月K线数据
        
        Args:
            symbol: 股票代码（如 "000001.SZ"）
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            KlineData对象列表
        """
        await self.rate_limiter.acquire()
        return await self.provider.get_kline(symbol, start_date, end_date, period="monthly")
