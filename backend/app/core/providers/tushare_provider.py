"""Tushare data provider implementation."""
import logging
from datetime import datetime
from typing import List, Optional
import tushare as ts
from .base import DataProvider
from ...models.data_models import KlineData, FundamentalData
from ...utils.data_converter import DataConverter
from ...core.config import settings
from ...core.exceptions import DataProviderError

logger = logging.getLogger(__name__)


class TushareProvider(DataProvider):
    """Tushare Pro API data provider."""

    def __init__(self, token: Optional[str] = None):
        """
        Initialize TushareProvider with API token.

        Args:
            token: Tushare Pro API token. If not provided, reads from settings.
        """
        self.token = token or settings.TUSHARE_TOKEN
        if not self.token:
            raise ValueError("Tushare token must be provided or set in TUSHARE_TOKEN environment variable")
        ts.set_token(self.token)
        self.pro = ts.pro_api()

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
            symbol: Stock symbol or code (e.g., "000001.SZ")
            start_date: Start date for data range
            end_date: End date for data range
            period: Data period (e.g., "daily", "weekly", "monthly")

        Returns:
            List of KlineData objects
        """
        # Convert datetime objects to Tushare format (YYYYMMDD)
        ts_start_date = start_date.strftime("%Y%m%d") if start_date else None
        ts_end_date = end_date.strftime("%Y%m%d") if end_date else None

        # Determine Tushare asset type and freq
        asset = "E"  # Stock
        freq = period
        if freq == "daily":
            freq = "D"
        elif freq == "weekly":
            freq = "W"
        elif freq == "monthly":
            freq = "M"

        try:
            # Get kline data from Tushare
            df = self.pro.pro_bar(
                ts_code=symbol,
                asset=asset,
                freq=freq,
                start_date=ts_start_date,
                end_date=ts_end_date,
                adj="qfq"  # Pre-adjusted
            )

            if df is None or df.empty:
                return []

            # Convert DataFrame to list of KlineData using DataConverter
            return DataConverter.tushare_kline_to_kline_data(df)

        except Exception as e:
            logger.error(f"Error getting kline data from Tushare: {e}", exc_info=True)
            raise DataProviderError("tushare", str(e), e) from e

    async def get_fundamental(self, symbol: str) -> Optional[FundamentalData]:
        """
        Get fundamental data for a symbol.

        Args:
            symbol: Stock symbol or code (e.g., "000001.SZ")

        Returns:
            FundamentalData object or None if not found
        """
        try:
            # Get daily basic data which includes fundamental metrics
            df = self.pro.daily_basic(ts_code=symbol, trade_date=datetime.now().strftime("%Y%m%d"))

            if df is None or df.empty:
                # Try to get the latest available data
                df = self.pro.daily_basic(ts_code=symbol, limit=1)

            if df is None or df.empty:
                return None

            # Get stock name from stock list
            name = None
            stock_list = self.pro.stock_basic(ts_code=symbol)
            if stock_list is not None and not stock_list.empty:
                name = stock_list.iloc[0]["name"]

            return DataConverter.tushare_daily_basic_to_fundamental_data(df, name)

        except Exception as e:
            logger.error(f"Error getting fundamental data from Tushare: {e}", exc_info=True)
            raise DataProviderError("tushare", str(e), e) from e

    async def search_symbol(self, keyword: str) -> List[str]:
        """
        Search for stock symbols by keyword.

        Args:
            keyword: Search keyword (symbol or name)

        Returns:
            List of matching symbols
        """
        try:
            # Get all stock basics
            df = self.pro.stock_basic()

            if df is None or df.empty:
                return []

            # Filter by keyword in symbol or name
            keyword_lower = keyword.lower()
            mask = (
                df["ts_code"].str.lower().str.contains(keyword_lower) |
                df["name"].str.lower().str.contains(keyword_lower)
            )
            matching_df = df[mask]

            return matching_df["ts_code"].tolist()

        except Exception as e:
            logger.error(f"Error searching symbols in Tushare: {e}", exc_info=True)
            raise DataProviderError("tushare", str(e), e) from e
