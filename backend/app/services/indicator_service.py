"""Technical indicator calculation service using pandas-ta-classic."""
import pandas as pd
import pandas_ta_classic as ta


class IndicatorService:
    """Service class for calculating technical indicators."""

    @staticmethod
    def _validate_dataframe(df: pd.DataFrame) -> bool:
        """
        Validate that DataFrame has required columns for indicator calculation.
        
        Args:
            df: Input DataFrame with OHLCV data
            
        Returns:
            True if DataFrame is valid, raises ValueError otherwise
        """
        required_columns = ["open", "high", "low", "close"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"DataFrame missing required columns: {missing_columns}")
        return True

    # ==================== Trend Indicators ====================

    @staticmethod
    def sma(df: pd.DataFrame, length: int = 10, source: str = "close") -> pd.DataFrame:
        """
        Calculate Simple Moving Average (SMA).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: SMA period
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with SMA values
        """
        IndicatorService._validate_dataframe(df)
        return ta.sma(close=df[source], length=length)

    @staticmethod
    def ema(df: pd.DataFrame, length: int = 10, source: str = "close") -> pd.DataFrame:
        """
        Calculate Exponential Moving Average (EMA).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: EMA period
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with EMA values
        """
        IndicatorService._validate_dataframe(df)
        return ta.ema(close=df[source], length=length)

    @staticmethod
    def wma(df: pd.DataFrame, length: int = 10, source: str = "close") -> pd.DataFrame:
        """
        Calculate Weighted Moving Average (WMA).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: WMA period
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with WMA values
        """
        IndicatorService._validate_dataframe(df)
        return ta.wma(close=df[source], length=length)

    @staticmethod
    def macd(
        df: pd.DataFrame,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9,
        source: str = "close"
    ) -> pd.DataFrame:
        """
        Calculate Moving Average Convergence Divergence (MACD).
        
        Args:
            df: Input DataFrame with OHLCV data
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with MACD, signal, and histogram values
        """
        IndicatorService._validate_dataframe(df)
        return ta.macd(close=df[source], fast=fast, slow=slow, signal=signal)

    @staticmethod
    def bollinger_bands(
        df: pd.DataFrame,
        length: int = 20,
        std: float = 2.0,
        source: str = "close"
    ) -> pd.DataFrame:
        """
        Calculate Bollinger Bands (BOLL).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: Period for middle band
            std: Standard deviation multiplier
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with upper, middle, and lower bands
        """
        IndicatorService._validate_dataframe(df)
        return ta.bbands(close=df[source], length=length, std=std)

    # ==================== Momentum Indicators ====================

    @staticmethod
    def rsi(df: pd.DataFrame, length: int = 14, source: str = "close") -> pd.DataFrame:
        """
        Calculate Relative Strength Index (RSI).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: RSI period
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with RSI values
        """
        IndicatorService._validate_dataframe(df)
        return ta.rsi(close=df[source], length=length)

    @staticmethod
    def kdj(
        df: pd.DataFrame,
        length: int = 14,
        signal: int = 3,
        smooth: int = 3
    ) -> pd.DataFrame:
        """
        Calculate KDJ (Stochastic Oscillator variant).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: KDJ period
            signal: Signal line period
            smooth: Smoothing period
            
        Returns:
            DataFrame with K, D, and J values
        """
        IndicatorService._validate_dataframe(df)
        # pandas-ta's stoch returns STOCHk and STOCHd, J = 3*K - 2*D
        stoch_df = ta.stoch(
            high=df["high"],
            low=df["low"],
            close=df["close"],
            k=length,
            d=signal,
            smooth_k=smooth
        )
        if stoch_df is not None and not stoch_df.empty:
            k_col = stoch_df.columns[0]
            d_col = stoch_df.columns[1]
            stoch_df["KDJ_J"] = 3 * stoch_df[k_col] - 2 * stoch_df[d_col]
        return stoch_df

    @staticmethod
    def stochastic(
        df: pd.DataFrame,
        k: int = 14,
        d: int = 3,
        smooth_k: int = 3
    ) -> pd.DataFrame:
        """
        Calculate Stochastic Oscillator.
        
        Args:
            df: Input DataFrame with OHLCV data
            k: %K period
            d: %D period
            smooth_k: %K smoothing period
            
        Returns:
            DataFrame with STOCHk and STOCHd values
        """
        IndicatorService._validate_dataframe(df)
        return ta.stoch(
            high=df["high"],
            low=df["low"],
            close=df["close"],
            k=k,
            d=d,
            smooth_k=smooth_k
        )

    @staticmethod
    def cci(df: pd.DataFrame, length: int = 20) -> pd.DataFrame:
        """
        Calculate Commodity Channel Index (CCI).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: CCI period
            
        Returns:
            DataFrame with CCI values
        """
        IndicatorService._validate_dataframe(df)
        return ta.cci(high=df["high"], low=df["low"], close=df["close"], length=length)

    @staticmethod
    def roc(df: pd.DataFrame, length: int = 10, source: str = "close") -> pd.DataFrame:
        """
        Calculate Rate of Change (ROC).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: ROC period
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with ROC values
        """
        IndicatorService._validate_dataframe(df)
        return ta.roc(close=df[source], length=length)

    # ==================== Volume Indicators ====================

    @staticmethod
    def volume(df: pd.DataFrame) -> pd.DataFrame:
        """
        Return volume data (VOL).
        
        Args:
            df: Input DataFrame with volume column
            
        Returns:
            DataFrame with volume values
        """
        if "volume" not in df.columns:
            raise ValueError("DataFrame missing 'volume' column")
        return pd.DataFrame({"volume": df["volume"]})

    @staticmethod
    def obv(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate On-Balance Volume (OBV).
        
        Args:
            df: Input DataFrame with OHLCV data
            
        Returns:
            DataFrame with OBV values
        """
        IndicatorService._validate_dataframe(df)
        if "volume" not in df.columns:
            raise ValueError("DataFrame missing 'volume' column")
        return ta.obv(close=df["close"], volume=df["volume"])

    @staticmethod
    def ad(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate Accumulation/Distribution Line (AD).
        
        Args:
            df: Input DataFrame with OHLCV data
            
        Returns:
            DataFrame with AD values
        """
        IndicatorService._validate_dataframe(df)
        if "volume" not in df.columns:
            raise ValueError("DataFrame missing 'volume' column")
        return ta.ad(high=df["high"], low=df["low"], close=df["close"], volume=df["volume"])

    @staticmethod
    def adx(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
        """
        Calculate Average Directional Index (ADX).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: ADX period
            
        Returns:
            DataFrame with ADX, DI+, and DI- values
        """
        IndicatorService._validate_dataframe(df)
        return ta.adx(high=df["high"], low=df["low"], close=df["close"], length=length)

    # ==================== Volatility Indicators ====================

    @staticmethod
    def atr(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
        """
        Calculate Average True Range (ATR).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: ATR period
            
        Returns:
            DataFrame with ATR values
        """
        IndicatorService._validate_dataframe(df)
        return ta.atr(high=df["high"], low=df["low"], close=df["close"], length=length)

    @staticmethod
    def donchian(df: pd.DataFrame, lower_length: int = 20, upper_length: int = 20) -> pd.DataFrame:
        """
        Calculate Donchian Channels.
        
        Args:
            df: Input DataFrame with OHLCV data
            lower_length: Lower band period
            upper_length: Upper band period
            
        Returns:
            DataFrame with DCB (lower), DCM (middle), and DCU (upper) bands
        """
        IndicatorService._validate_dataframe(df)
        return ta.donchian(
            high=df["high"],
            low=df["low"],
            lower_length=lower_length,
            upper_length=upper_length
        )

    # ==================== Additional Indicators (to reach 30+) ====================

    @staticmethod
    def tema(df: pd.DataFrame, length: int = 10, source: str = "close") -> pd.DataFrame:
        """
        Calculate Triple Exponential Moving Average (TEMA).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: TEMA period
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with TEMA values
        """
        IndicatorService._validate_dataframe(df)
        return ta.tema(close=df[source], length=length)

    @staticmethod
    def kama(df: pd.DataFrame, length: int = 10, source: str = "close") -> pd.DataFrame:
        """
        Calculate Kaufman's Adaptive Moving Average (KAMA).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: KAMA period
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with KAMA values
        """
        IndicatorService._validate_dataframe(df)
        return ta.kama(close=df[source], length=length)

    @staticmethod
    def mama(df: pd.DataFrame, source: str = "close") -> pd.DataFrame:
        """
        Calculate MESA Adaptive Moving Average (MAMA).
        
        Args:
            df: Input DataFrame with OHLCV data
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with MAMA and FAMA values
        """
        IndicatorService._validate_dataframe(df)
        return ta.mama(close=df[source])

    @staticmethod
    def vwap(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate Volume Weighted Average Price (VWAP).
        
        Args:
            df: Input DataFrame with OHLCV data
            
        Returns:
            DataFrame with VWAP values
        """
        IndicatorService._validate_dataframe(df)
        if "volume" not in df.columns:
            raise ValueError("DataFrame missing 'volume' column")
        return ta.vwap(high=df["high"], low=df["low"], close=df["close"], volume=df["volume"])

    @staticmethod
    def rvi(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
        """
        Calculate Relative Vigor Index (RVI).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: RVI period
            
        Returns:
            DataFrame with RVI and signal values
        """
        IndicatorService._validate_dataframe(df)
        return ta.rvi(close=df["close"], length=length)

    @staticmethod
    def trix(df: pd.DataFrame, length: int = 15, source: str = "close") -> pd.DataFrame:
        """
        Calculate TRIX.
        
        Args:
            df: Input DataFrame with OHLCV data
            length: TRIX period
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with TRIX values
        """
        IndicatorService._validate_dataframe(df)
        return ta.trix(close=df[source], length=length)

    @staticmethod
    def ppo(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9, source: str = "close") -> pd.DataFrame:
        """
        Calculate Percentage Price Oscillator (PPO).
        
        Args:
            df: Input DataFrame with OHLCV data
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with PPO, signal, and histogram values
        """
        IndicatorService._validate_dataframe(df)
        return ta.ppo(close=df[source], fast=fast, slow=slow, signal=signal)

    @staticmethod
    def cmo(df: pd.DataFrame, length: int = 14, source: str = "close") -> pd.DataFrame:
        """
        Calculate Chande Momentum Oscillator (CMO).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: CMO period
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with CMO values
        """
        IndicatorService._validate_dataframe(df)
        return ta.cmo(close=df[source], length=length)

    @staticmethod
    def ultosc(df: pd.DataFrame, fast: int = 7, medium: int = 14, slow: int = 28) -> pd.DataFrame:
        """
        Calculate Ultimate Oscillator (ULTOSC).
        
        Args:
            df: Input DataFrame with OHLCV data
            fast: Fast period
            medium: Medium period
            slow: Slow period
            
        Returns:
            DataFrame with ULTOSC values
        """
        IndicatorService._validate_dataframe(df)
        return ta.ultosc(high=df["high"], low=df["low"], close=df["close"], fast=fast, medium=medium, slow=slow)

    @staticmethod
    def willr(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
        """
        Calculate Williams %R (WILLR).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: Williams %R period
            
        Returns:
            DataFrame with WILLR values
        """
        IndicatorService._validate_dataframe(df)
        return ta.willr(high=df["high"], low=df["low"], close=df["close"], length=length)

    @staticmethod
    def ao(df: pd.DataFrame, fast: int = 5, slow: int = 34) -> pd.DataFrame:
        """
        Calculate Awesome Oscillator (AO).
        
        Args:
            df: Input DataFrame with OHLCV data
            fast: Fast period
            slow: Slow period
            
        Returns:
            DataFrame with AO values
        """
        IndicatorService._validate_dataframe(df)
        return ta.ao(high=df["high"], low=df["low"], fast=fast, slow=slow)

    @staticmethod
    def kst(
        df: pd.DataFrame,
        roc1: int = 10,
        roc2: int = 15,
        roc3: int = 20,
        roc4: int = 30,
        sma1: int = 10,
        sma2: int = 10,
        sma3: int = 10,
        sma4: int = 15,
        signal: int = 9,
        source: str = "close"
    ) -> pd.DataFrame:
        """
        Calculate Know Sure Thing (KST).
        
        Args:
            df: Input DataFrame with OHLCV data
            roc1-roc4: ROC periods
            sma1-sma4: SMA periods for ROCs
            signal: Signal line period
            source: Source column for calculation (default: close)
            
        Returns:
            DataFrame with KST and signal values
        """
        IndicatorService._validate_dataframe(df)
        return ta.kst(
            close=df[source],
            roc1=roc1,
            roc2=roc2,
            roc3=roc3,
            roc4=roc4,
            sma1=sma1,
            sma2=sma2,
            sma3=sma3,
            sma4=sma4,
            signal=signal
        )

    @staticmethod
    def ichimoku(
        df: pd.DataFrame,
        tenkan: int = 9,
        kijun: int = 26,
        senkou: int = 52,
        offset: int = 26
    ) -> pd.DataFrame:
        """
        Calculate Ichimoku Kinko Hyo.
        
        Args:
            df: Input DataFrame with OHLCV data
            tenkan: Tenkan-sen period
            kijun: Kijun-sen period
            senkou: Senkou span B period
            offset: Chikou span offset
            
        Returns:
            DataFrame with Ichimoku components
        """
        IndicatorService._validate_dataframe(df)
        return ta.ichimoku(
            high=df["high"],
            low=df["low"],
            close=df["close"],
            tenkan=tenkan,
            kijun=kijun,
            senkou=senkou,
            offset=offset
        )

    @staticmethod
    def mfi(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
        """
        Calculate Money Flow Index (MFI).
        
        Args:
            df: Input DataFrame with OHLCV data
            length: MFI period (default: 14)
            
        Returns:
            DataFrame with MFI values
        """
        IndicatorService._validate_dataframe(df)
        if "volume" not in df.columns:
            raise ValueError("DataFrame missing 'volume' column")
        return ta.mfi(
            high=df["high"],
            low=df["low"],
            close=df["close"],
            volume=df["volume"],
            length=length
        )
