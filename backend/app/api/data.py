"""Data API endpoints for K-line data and technical indicators."""
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
import pandas as pd

from app.services.kline_service import KlineDataService
from app.services.indicator_service import IndicatorService
from app.models.data_models import KlineData

router = APIRouter()


# ==================== Request/Response Models ====================

class DateRangeParams(BaseModel):
    """Date range parameters for data queries."""
    start_date: Optional[datetime] = Field(
        None, 
        description="Start date (inclusive). Format: YYYY-MM-DD"
    )
    end_date: Optional[datetime] = Field(
        None, 
        description="End date (inclusive). Format: YYYY-MM-DD"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "start_date": "2024-01-01",
                "end_date": "2024-12-31"
            }
        }


class KlineResponse(BaseModel):
    """Response model for K-line data."""
    symbol: str = Field(..., description="Stock symbol")
    data: List[KlineData] = Field(..., description="List of K-line data points")
    count: int = Field(..., description="Number of data points returned")
    
    class Config:
        schema_extra = {
            "example": {
                "symbol": "000001.SZ",
                "count": 100,
                "data": [
                    {
                        "symbol": "000001.SZ",
                        "timestamp": "2024-01-02T00:00:00",
                        "open": 10.5,
                        "high": 11.0,
                        "low": 10.3,
                        "close": 10.8,
                        "volume": 1000000,
                        "amount": 10800000
                    }
                ]
            }
        }


class IndicatorParams(BaseModel):
    """Parameters for technical indicator calculation."""
    indicator: str = Field(
        ..., 
        description="Indicator name (e.g., 'sma', 'ema', 'rsi', 'macd')"
    )
    length: Optional[int] = Field(
        None, 
        description="Period length for the indicator"
    )
    source: Optional[str] = Field(
        "close", 
        description="Source column for calculation (e.g., 'close', 'open')"
    )
    fast: Optional[int] = Field(None, description="Fast period (for MACD, etc.)")
    slow: Optional[int] = Field(None, description="Slow period (for MACD, etc.)")
    signal: Optional[int] = Field(None, description="Signal period (for MACD, etc.)")
    std: Optional[float] = Field(None, description="Standard deviation (for Bollinger Bands)")
    # Additional parameters can be added as needed
    
    class Config:
        schema_extra = {
            "example": {
                "indicator": "sma",
                "length": 20,
                "source": "close"
            }
        }


class IndicatorResponse(BaseModel):
    """Response model for technical indicator data."""
    symbol: str = Field(..., description="Stock symbol")
    indicator: str = Field(..., description="Indicator name")
    parameters: Dict[str, Any] = Field(..., description="Parameters used for calculation")
    data: List[Dict[str, Any]] = Field(..., description="Indicator values with timestamps")
    
    class Config:
        schema_extra = {
            "example": {
                "symbol": "000001.SZ",
                "indicator": "sma",
                "parameters": {"length": 20, "source": "close"},
                "data": [
                    {"timestamp": "2024-01-02T00:00:00", "value": 10.5},
                    {"timestamp": "2024-01-03T00:00:00", "value": 10.6}
                ]
            }
        }


class HealthResponse(BaseModel):
    """Extended health response including data service status."""
    status: str = Field(..., description="Overall system status")
    data_services: Dict[str, str] = Field(..., description="Status of data services")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "data_services": {
                    "kline_service": "available",
                    "indicator_service": "available"
                }
            }
        }


# ==================== Dependencies ====================

def get_kline_service() -> KlineDataService:
    """Dependency for KlineDataService."""
    try:
        return KlineDataService()
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=503,
            detail=f"Kline data service unavailable: {str(e)}"
        )


def get_indicator_service() -> IndicatorService:
    """Dependency for IndicatorService."""
    try:
        return IndicatorService()
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=503,
            detail=f"Indicator service unavailable: {str(e)}"
        )


# ==================== API Endpoints ====================

@router.get("/health", response_model=HealthResponse, tags=["data"])
async def data_health_check():
    """
    Health check for data services.
    
    Returns status of K-line data service and technical indicator service.
    """
    try:
        # Try to create KlineDataService instance
        KlineDataService()
        kline_status = "available"
    except Exception as e:
        kline_status = f"error: {str(e)}"
    
    try:
        # Try to create IndicatorService instance
        IndicatorService()
        indicator_status = "available"
    except Exception as e:
        indicator_status = f"error: {str(e)}"
    
    overall_status = "healthy" if "available" in [kline_status, indicator_status] else "degraded"
    
    return HealthResponse(
        status=overall_status,
        data_services={
            "kline_service": kline_status,
            "indicator_service": indicator_status
        }
    )


@router.get("/kline/{symbol}", response_model=KlineResponse, tags=["data"])
async def get_kline_data(
    symbol: str,
    start_date: Optional[datetime] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="End date (YYYY-MM-DD)"),
    period: str = Query("daily", description="K-line period: daily, weekly, monthly"),
    kline_service: KlineDataService = Depends(get_kline_service)
):
    """
    Get K-line data for a specific symbol.
    
    - **symbol**: Stock symbol (e.g., "000001.SZ")
    - **start_date**: Optional start date (inclusive)
    - **end_date**: Optional end date (inclusive)
    - **period**: K-line period (daily, weekly, monthly)
    
    Returns K-line data including OHLCV (open, high, low, close, volume).
    """
    try:
        # Validate symbol format (basic validation)
        if not symbol or "." not in symbol:
            raise HTTPException(
                status_code=400,
                detail="Symbol must be in format 'CODE.EXCHANGE' (e.g., '000001.SZ')"
            )
        
        # Validate period
        period_map = {
            "daily": kline_service.get_daily_kline,
            "weekly": kline_service.get_weekly_kline,
            "monthly": kline_service.get_monthly_kline
        }
        
        if period not in period_map:
            raise HTTPException(
                status_code=400,
                detail=f"Period must be one of: {list(period_map.keys())}"
            )
        
        # Get K-line data
        kline_data = await period_map[period](symbol, start_date, end_date)
        
        if not kline_data:
            raise HTTPException(
                status_code=404,
                detail=f"No K-line data found for symbol '{symbol}' in the specified date range"
            )
        
        return KlineResponse(
            symbol=symbol,
            data=kline_data,
            count=len(kline_data)
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/indicators/{symbol}", response_model=IndicatorResponse, tags=["data"])
async def calculate_indicator(
    symbol: str,
    indicator: str = Query(..., description="Indicator name (e.g., 'sma', 'rsi', 'macd')"),
    length: Optional[int] = Query(None, description="Period length"),
    source: Optional[str] = Query("close", description="Source column (e.g., 'close', 'open')"),
    fast: Optional[int] = Query(None, description="Fast period (for MACD, etc.)"),
    slow: Optional[int] = Query(None, description="Slow period (for MACD, etc.)"),
    signal: Optional[int] = Query(None, description="Signal period (for MACD, etc.)"),
    std: Optional[float] = Query(None, description="Standard deviation (for Bollinger Bands)"),
    start_date: Optional[datetime] = Query(None, description="Start date for K-line data"),
    end_date: Optional[datetime] = Query(None, description="End date for K-line data"),
    kline_service: KlineDataService = Depends(get_kline_service),
    indicator_service: IndicatorService = Depends(get_indicator_service)
):
    """
    Calculate technical indicator for a specific symbol.
    
    - **symbol**: Stock symbol (e.g., "000001.SZ")
    - **indicator**: Indicator name (see available indicators in documentation)
    - **length**: Period length for the indicator
    - **source**: Source column for calculation
    - Additional parameters depend on the specific indicator
    
    Returns calculated indicator values with timestamps.
    """
    try:
        # First, get K-line data
        kline_data = await kline_service.get_daily_kline(symbol, start_date, end_date)
        
        if not kline_data:
            raise HTTPException(
                status_code=404,
                detail=f"No K-line data found for symbol '{symbol}' in the specified date range"
            )
        
        # Convert KlineData list to DataFrame
        df_data = []
        for k in kline_data:
            row = {
                "timestamp": k.timestamp,
                "open": k.open,
                "high": k.high,
                "low": k.low,
                "close": k.close
            }
            if k.volume is not None:
                row["volume"] = k.volume
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        
        # Map indicator names to service methods
        indicator_map = {
            "sma": indicator_service.sma,
            "ema": indicator_service.ema,
            "wma": indicator_service.wma,
            "macd": indicator_service.macd,
            "bollinger_bands": indicator_service.bollinger_bands,
            "rsi": indicator_service.rsi,
            "kdj": indicator_service.kdj,
            "stochastic": indicator_service.stochastic,
            "cci": indicator_service.cci,
            "roc": indicator_service.roc,
            "volume": indicator_service.volume,
            "obv": indicator_service.obv,
            "ad": indicator_service.ad,
            "adx": indicator_service.adx,
            "atr": indicator_service.atr,
            "donchian": indicator_service.donchian,
            "tema": indicator_service.tema,
            "kama": indicator_service.kama,
            "mama": indicator_service.mama,
            "vwap": indicator_service.vwap,
            "rvi": indicator_service.rvi,
            "trix": indicator_service.trix,
            "ppo": indicator_service.ppo,
            "cmo": indicator_service.cmo,
            "ultosc": indicator_service.ultosc,
            "willr": indicator_service.willr,
            "ao": indicator_service.ao,
            "kst": indicator_service.kst,
            "ichimoku": indicator_service.ichimoku,
            "mfi": indicator_service.mfi
        }
        
        if indicator not in indicator_map:
            available = list(indicator_map.keys())
            raise HTTPException(
                status_code=400,
                detail=f"Unknown indicator '{indicator}'. Available indicators: {available}"
            )
        
        # Prepare parameters for the indicator method
        method = indicator_map[indicator]
        
        # Get method signature to determine required parameters
        import inspect
        sig = inspect.signature(method)
        params = {}
        
        # Add df parameter
        params["df"] = df
        
        # Add other parameters based on method signature
        param_names = list(sig.parameters.keys())
        
        if "length" in param_names and length is not None:
            params["length"] = length
        if "source" in param_names and source is not None:
            params["source"] = source
        if "fast" in param_names and fast is not None:
            params["fast"] = fast
        if "slow" in param_names and slow is not None:
            params["slow"] = slow
        if "signal" in param_names and signal is not None:
            params["signal"] = signal
        if "std" in param_names and std is not None:
            params["std"] = std
        
        # Calculate indicator
        result_df = method(**params)
        
        if result_df is None or result_df.empty:
            raise HTTPException(
                status_code=500,
                detail=f"Indicator calculation returned no data for '{indicator}'"
            )
        
        # Convert result to response format
        data = []
        for idx, (timestamp, row) in enumerate(zip(df["timestamp"], result_df.itertuples(index=False))):
            # Convert row to dict
            row_dict = {}
            for col_idx, col_name in enumerate(result_df.columns):
                value = getattr(row, col_idx) if hasattr(row, col_idx) else row[col_idx]
                row_dict[col_name] = float(value) if pd.notna(value) else None
            
            data.append({
                "timestamp": timestamp.isoformat() if hasattr(timestamp, "isoformat") else str(timestamp),
                "values": row_dict
            })
        
        # Prepare parameters used
        parameters_used = {k: v for k, v in {
            "length": length,
            "source": source,
            "fast": fast,
            "slow": slow,
            "signal": signal,
            "std": std
        }.items() if v is not None}
        
        return IndicatorResponse(
            symbol=symbol,
            indicator=indicator,
            parameters=parameters_used,
            data=data
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )