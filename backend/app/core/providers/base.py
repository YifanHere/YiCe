"""Base class for data providers."""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from ...models.data_models import KlineData, FundamentalData


class DataProvider(ABC):
    """Abstract base class for financial data providers."""
    
    @abstractmethod
    async def get_kline(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        period: str = "daily"
    ) -> List[KlineData]:
        """
        Get kline (candlestick) data for a symbol.
        
        Args:
            symbol: Stock symbol or code
            start_date: Start date for data range
            end_date: End date for data range
            period: Data period (e.g., "daily", "weekly", "monthly")
            
        Returns:
            List of KlineData objects
        """
        pass
    
    @abstractmethod
    async def get_fundamental(self, symbol: str) -> Optional[FundamentalData]:
        """
        Get fundamental data for a symbol.
        
        Args:
            symbol: Stock symbol or code
            
        Returns:
            FundamentalData object or None if not found
        """
        pass
    
    @abstractmethod
    async def search_symbol(self, keyword: str) -> List[str]:
        """
        Search for stock symbols by keyword.
        
        Args:
            keyword: Search keyword
            
        Returns:
            List of matching symbols
        """
        pass
