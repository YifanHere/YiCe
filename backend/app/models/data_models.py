"""Data models for financial data."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class KlineData(BaseModel):
    """Kline (candlestick) data model."""
    symbol: str = Field(..., description="Stock symbol or code")
    timestamp: datetime = Field(..., description="Timestamp of the kline")
    open: float = Field(..., description="Opening price")
    high: float = Field(..., description="Highest price")
    low: float = Field(..., description="Lowest price")
    close: float = Field(..., description="Closing price")
    volume: Optional[float] = Field(None, description="Trading volume")
    amount: Optional[float] = Field(None, description="Trading amount")


class FundamentalData(BaseModel):
    """Fundamental data model."""
    symbol: str = Field(..., description="Stock symbol or code")
    name: Optional[str] = Field(None, description="Company name")
    pe_ratio: Optional[float] = Field(None, description="Price-to-Earnings ratio")
    pb_ratio: Optional[float] = Field(None, description="Price-to-Book ratio")
    market_cap: Optional[float] = Field(None, description="Market capitalization")
    total_shares: Optional[float] = Field(None, description="Total outstanding shares")
    float_shares: Optional[float] = Field(None, description="Floating shares")
