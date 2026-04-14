"""Fundamental data service layer."""
from typing import Optional, List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging
from ..core.providers.factory import DataSourceFactory
from ..core.providers.tushare_provider import TushareProvider
from ..core.exceptions import DataServiceError
from ..core.cache_strategy import cached, DataType

logger = logging.getLogger(__name__)


class FundamentalDataService:
    """Service for retrieving fundamental financial data."""
    
    def __init__(self):
        """Initialize the fundamental data service."""
        self.provider: Optional[TushareProvider] = None
        self._init_provider()
    
    def _init_provider(self):
        """Initialize the data provider."""
        try:
            provider = DataSourceFactory.get_provider("tushare")
            if isinstance(provider, TushareProvider):
                self.provider = provider
            else:
                logger.error("Failed to get TushareProvider")
        except Exception as e:
            logger.error(f"Error initializing data provider: {e}")
            raise DataServiceError("FundamentalDataService", f"Failed to initialize provider: {e}", e) from e
    
    @cached(provider="tushare", data_type=DataType.FUNDAMENTAL, exclude_params=["self"])
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def get_financial_report(
        self,
        symbol: str,
        report_type: str = "balance",
        period: Optional[str] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get financial report data (balance sheet, income statement, cash flow).
        
        Args:
            symbol: Stock symbol (e.g., "000001.SZ")
            report_type: Type of report (balance, income, cashflow)
            period: Report period (YYYYMMDD), latest if None
            
        Returns:
            List of financial report records or None
        """
        if not self.provider:
            logger.error("Data provider not initialized")
            return None
        
        try:
            pro = self.provider.pro
            
            # Map report type to Tushare API
            api_map = {
                "balance": pro.balancesheet,
                "income": pro.income,
                "cashflow": pro.cashflow
            }
            
            api_func = api_map.get(report_type)
            if not api_func:
                logger.error(f"Invalid report type: {report_type}")
                return None
            
            # Fetch data
            params = {"ts_code": symbol}
            if period:
                params["end_date"] = period
            else:
                params["limit"] = 5  # Get latest 5 reports
            
            df = api_func(**params)
            
            if df is None or df.empty:
                return None
            
            # Convert to standardized dict format
            records = df.to_dict("records")
            
            # Standardize date fields
            for record in records:
                if "end_date" in record and record["end_date"]:
                    record["report_date"] = record["end_date"]
            
            return records
            
        except Exception as e:
            logger.error(f"Error getting financial report for {symbol}: {e}")
            raise DataServiceError("FundamentalDataService", f"Failed to get financial report: {e}", e) from e
    
    @cached(provider="tushare", data_type=DataType.FUNDAMENTAL, exclude_params=["self"])
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def get_company_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get basic company information.
        
        Args:
            symbol: Stock symbol (e.g., "000001.SZ")
            
        Returns:
            Company info dict or None
        """
        if not self.provider:
            logger.error("Data provider not initialized")
            return None
        
        try:
            df = self.provider.pro.stock_basic(ts_code=symbol)
            
            if df is None or df.empty:
                return None
            
            record = df.iloc[0].to_dict()
            
            # Standardize fields
            standardized = {
                "symbol": record.get("ts_code"),
                "name": record.get("name"),
                "area": record.get("area"),
                "industry": record.get("industry"),
                "market": record.get("market"),
                "list_date": record.get("list_date"),
                "fullname": record.get("fullname"),
                "enname": record.get("enname"),
                "exchange": record.get("exchange"),
                "curr_type": record.get("curr_type")
            }
            
            return standardized
            
        except Exception as e:
            logger.error(f"Error getting company info for {symbol}: {e}")
            raise DataServiceError("FundamentalDataService", f"Failed to get company info: {e}", e) from e
    
    @cached(provider="tushare", data_type=DataType.FUNDAMENTAL, exclude_params=["self"])
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def get_industry_classification(
        self,
        symbol: Optional[str] = None,
        industry_level: str = "L1"
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get industry classification data.
        
        Args:
            symbol: Stock symbol, returns all industries if None
            industry_level: Industry level (L1, L2, L3)
            
        Returns:
            List of industry classification records or None
        """
        if not self.provider:
            logger.error("Data provider not initialized")
            return None
        
        try:
            # Get SW (Shenwan) industry classification
            df = self.provider.pro.index_classify(level=industry_level, src="SW")
            
            if df is None or df.empty:
                return None
            
            records = df.to_dict("records")
            
            # If symbol provided, filter to that symbol's industry
            if symbol:
                # Get symbol's industry membership
                member_df = self.provider.pro.index_member(index_code=records[0]["index_code"] if records else "")
                if member_df is not None and not member_df.empty:
                    symbol_member = member_df[member_df["con_code"] == symbol]
                    if not symbol_member.empty:
                        # Get industry info for that index
                        index_code = symbol_member.iloc[0]["index_code"]
                        industry_info = next((r for r in records if r["index_code"] == index_code), None)
                        return [industry_info] if industry_info else None
            
            return records
            
        except Exception as e:
            logger.error(f"Error getting industry classification: {e}")
            raise DataServiceError("FundamentalDataService", f"Failed to get industry classification: {e}", e) from e
