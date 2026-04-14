"""Data conversion utilities for financial data."""
from datetime import datetime
from typing import List, Type, TypeVar, Optional
import pandas as pd
from pydantic import BaseModel

from ..models.data_models import KlineData, FundamentalData

T = TypeVar('T', bound=BaseModel)


class DataConverter:
    """Converter for transforming data between different formats."""

    @staticmethod
    def tushare_kline_to_kline_data(df: pd.DataFrame) -> List[KlineData]:
        """
        Convert Tushare kline DataFrame to list of KlineData models.

        Args:
            df: Tushare pro_bar DataFrame

        Returns:
            List of KlineData objects in chronological order
        """
        if df is None or df.empty:
            return []

        kline_list = []
        for _, row in df.iterrows():
            kline = KlineData(
                symbol=row["ts_code"],
                timestamp=datetime.strptime(str(row["trade_date"]), "%Y%m%d"),
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=float(row["vol"]) if "vol" in row and pd.notna(row["vol"]) else None,
                amount=float(row["amount"]) if "amount" in row and pd.notna(row["amount"]) else None
            )
            kline_list.append(kline)

        # Reverse to get chronological order (Tushare returns newest first)
        kline_list.reverse()
        return kline_list

    @staticmethod
    def tushare_daily_basic_to_fundamental_data(
        df: pd.DataFrame,
        name: Optional[str] = None
    ) -> Optional[FundamentalData]:
        """
        Convert Tushare daily_basic DataFrame to FundamentalData model.

        Args:
            df: Tushare daily_basic DataFrame
            name: Optional company name

        Returns:
            FundamentalData object or None
        """
        if df is None or df.empty:
            return None

        row = df.iloc[0]
        return FundamentalData(
            symbol=row["ts_code"],
            name=name,
            pe_ratio=float(row["pe"]) if "pe" in row and pd.notna(row["pe"]) else None,
            pb_ratio=float(row["pb"]) if "pb" in row and pd.notna(row["pb"]) else None,
            market_cap=float(row["total_mv"]) if "total_mv" in row and pd.notna(row["total_mv"]) else None,
            total_shares=float(row["total_share"]) if "total_share" in row and pd.notna(row["total_share"]) else None,
            float_shares=float(row["float_share"]) if "float_share" in row and pd.notna(row["float_share"]) else None
        )

    @staticmethod
    def dataframe_to_models(df: pd.DataFrame, model_class: Type[T]) -> List[T]:
        """
        Convert a pandas DataFrame to a list of Pydantic models.

        Args:
            df: Input DataFrame
            model_class: Pydantic model class to convert to

        Returns:
            List of Pydantic model instances
        """
        if df is None or df.empty:
            return []

        # Convert DataFrame to list of dicts and then to models
        records = df.to_dict(orient="records")
        return [model_class(**record) for record in records]

    @staticmethod
    def models_to_dataframe(models: List[T]) -> pd.DataFrame:
        """
        Convert a list of Pydantic models to a pandas DataFrame.

        Args:
            models: List of Pydantic model instances

        Returns:
            pandas DataFrame
        """
        if not models:
            return pd.DataFrame()

        # Convert models to list of dicts and then to DataFrame
        records = [model.model_dump() for model in models]
        return pd.DataFrame(records)
