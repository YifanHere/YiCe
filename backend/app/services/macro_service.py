"""Macro economic data service."""
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
import pandas as pd
from ..core.providers.factory import DataSourceFactory
from ..core.providers.tushare_provider import TushareProvider
from ..core.exceptions import DataServiceError
from ..core.cache_strategy import cached, DataType

logger = logging.getLogger(__name__)


class MacroDataService:
    """Service for retrieving macro economic data."""

    def __init__(self):
        """Initialize MacroDataService with data provider."""
        self.provider: Optional[TushareProvider] = DataSourceFactory.get_provider("tushare")
        if not self.provider:
            raise ValueError("Tushare provider not available")

    @cached(provider="tushare", data_type=DataType.MACRO, exclude_params=["self"])
    async def get_gdp(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Get GDP (Gross Domestic Product) data.

        Args:
            start_date: Start date for data range
            end_date: End date for data range

        Returns:
            List of GDP data records
        """
        try:
            # Convert dates to Tushare format (YYYYMMDD)
            ts_start = start_date.strftime("%Y%m%d") if start_date else None
            ts_end = end_date.strftime("%Y%m%d") if end_date else None

            # Get GDP data from Tushare (using cn_gdp API)
            df = self.provider.pro.cn_gdp(
                start_date=ts_start,
                end_date=ts_end
            )

            if df is None or df.empty:
                return []

            # 向量化转换：将数值列转换为浮点数
            numeric_cols = ['gdp', 'gdp_yoy', 'pi', 'pi_yoy', 'si', 'si_yoy', 'ti', 'ti_yoy']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 转换为字典列表
            records = df.to_dict('records')
            result = []
            for record in records:
                result.append({
                    'date': record.get('date'),
                    'year': record.get('year'),
                    'quarter': record.get('quarter'),
                    'gdp': record.get('gdp'),
                    'gdp_yoy': record.get('gdp_yoy'),
                    'pi': record.get('pi'),
                    'pi_yoy': record.get('pi_yoy'),
                    'si': record.get('si'),
                    'si_yoy': record.get('si_yoy'),
                    'ti': record.get('ti'),
                    'ti_yoy': record.get('ti_yoy'),
                })
            return result

        except Exception as e:
            logger.error(f"Error getting GDP data: {e}", exc_info=True)
            raise DataServiceError("MacroDataService", f"Failed to get GDP data: {e}", e) from e

    @cached(provider="tushare", data_type=DataType.MACRO, exclude_params=["self"])
    async def get_cpi(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Get CPI (Consumer Price Index) data.

        Args:
            start_date: Start date for data range
            end_date: End date for data range

        Returns:
            List of CPI data records
        """
        try:
            ts_start = start_date.strftime("%Y%m%d") if start_date else None
            ts_end = end_date.strftime("%Y%m%d") if end_date else None

            # Get CPI data from Tushare (using cn_cpi API)
            df = self.provider.pro.cn_cpi(
                start_date=ts_start,
                end_date=ts_end
            )

            if df is None or df.empty:
                return []

            # 向量化转换：将数值列转换为浮点数
            numeric_cols = ['cpi', 'cpi_nt', 'cpi_t', 'cpi_food', 'cpi_notfood']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 转换为字典列表
            records = df.to_dict('records')
            result = []
            for record in records:
                result.append({
                    'date': record.get('date'),
                    'month': record.get('month'),
                    'cpi': record.get('cpi'),
                    'cpi_nt': record.get('cpi_nt'),
                    'cpi_t': record.get('cpi_t'),
                    'cpi_food': record.get('cpi_food'),
                    'cpi_notfood': record.get('cpi_notfood'),
                })
            return result

        except Exception as e:
            logger.error(f"Error getting CPI data: {e}", exc_info=True)
            raise DataServiceError("MacroDataService", f"Failed to get CPI data: {e}", e) from e

    @cached(provider="tushare", data_type=DataType.MACRO, exclude_params=["self"])
    async def get_ppi(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Get PPI (Producer Price Index) data.

        Args:
            start_date: Start date for data range
            end_date: End date for data range

        Returns:
            List of PPI data records
        """
        try:
            ts_start = start_date.strftime("%Y%m%d") if start_date else None
            ts_end = end_date.strftime("%Y%m%d") if end_date else None

            # Get PPI data from Tushare (using cn_ppi API)
            df = self.provider.pro.cn_ppi(
                start_date=ts_start,
                end_date=ts_end
            )

            if df is None or df.empty:
                return []

            # 向量化转换：将数值列转换为浮点数
            numeric_cols = ['ppi', 'ppi_mp', 'ppi_pi', 'ppi_rm', 'ppi_ru']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 转换为字典列表
            records = df.to_dict('records')
            result = []
            for record in records:
                result.append({
                    'date': record.get('date'),
                    'month': record.get('month'),
                    'ppi': record.get('ppi'),
                    'ppi_mp': record.get('ppi_mp'),
                    'ppi_pi': record.get('ppi_pi'),
                    'ppi_rm': record.get('ppi_rm'),
                    'ppi_ru': record.get('ppi_ru'),
                })
            return result

        except Exception as e:
            logger.error(f"Error getting PPI data: {e}", exc_info=True)
            raise DataServiceError("MacroDataService", f"Failed to get PPI data: {e}", e) from e

    @cached(provider="tushare", data_type=DataType.MACRO, exclude_params=["self"])
    async def get_interest_rate(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Get market interest rate data.

        Args:
            start_date: Start date for data range
            end_date: End date for data range

        Returns:
            List of interest rate data records
        """
        try:
            ts_start = start_date.strftime("%Y%m%d") if start_date else None
            ts_end = end_date.strftime("%Y%m%d") if end_date else None

            # Get SHIBOR (Shanghai Interbank Offered Rate) data
            df = self.provider.pro.shibor(
                start_date=ts_start,
                end_date=ts_end
            )

            if df is None or df.empty:
                return []

            # 向量化转换：将数值列转换为浮点数
            numeric_cols = ['on', '1w', '2w', '1m', '3m', '6m', '9m', '1y']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 转换为字典列表，保留NaN（将在JSON中变为null）
            records = df.to_dict('records')
            result = []
            for record in records:
                result.append({
                    'date': record.get('date'),
                    'on': record.get('on'),
                    '1w': record.get('1w'),
                    '2w': record.get('2w'),
                    '1m': record.get('1m'),
                    '3m': record.get('3m'),
                    '6m': record.get('6m'),
                    '9m': record.get('9m'),
                    '1y': record.get('1y'),
                })
            return result

        except Exception as e:
            logger.error(f"Error getting interest rate data: {e}", exc_info=True)
            raise DataServiceError("MacroDataService", f"Failed to get interest rate data: {e}", e) from e

    @cached(provider="tushare", data_type=DataType.MACRO, exclude_params=["self"])
    async def get_money_supply(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Get money supply data (M0, M1, M2).

        Args:
            start_date: Start date for data range
            end_date: End date for data range

        Returns:
            List of money supply data records
        """
        try:
            ts_start = start_date.strftime("%Y%m%d") if start_date else None
            ts_end = end_date.strftime("%Y%m%d") if end_date else None

            # Get money supply data from Tushare (using cn_m API)
            df = self.provider.pro.cn_m(
                start_date=ts_start,
                end_date=ts_end
            )

            if df is None or df.empty:
                return []

            # 向量化转换：将数值列转换为浮点数
            numeric_cols = ['m0', 'm0_yoy', 'm1', 'm1_yoy', 'm2', 'm2_yoy']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 转换为字典列表
            records = df.to_dict('records')
            result = []
            for record in records:
                result.append({
                    'date': record.get('date'),
                    'month': record.get('month'),
                    'm0': record.get('m0'),
                    'm0_yoy': record.get('m0_yoy'),
                    'm1': record.get('m1'),
                    'm1_yoy': record.get('m1_yoy'),
                    'm2': record.get('m2'),
                    'm2_yoy': record.get('m2_yoy'),
                })

            return result

        except Exception as e:
            logger.error(f"Error getting money supply data: {e}", exc_info=True)
            raise DataServiceError("MacroDataService", f"Failed to get money supply data: {e}", e) from e
