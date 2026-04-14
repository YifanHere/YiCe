"""Unit tests for technical indicator calculation service."""
from datetime import datetime, timedelta
from typing import List, Dict, Any
import pytest
import pandas as pd
import numpy as np
import pandas_ta_classic as ta

# Import services to test
from app.services.indicator_service import IndicatorService
from app.services.custom_indicator import CustomIndicator, CustomIndicatorManager, indicator_manager


class TestIndicatorService:
    """Test IndicatorService class."""

    @pytest.fixture
    def sample_ohlcv_df(self):
        """Create sample OHLCV DataFrame for testing."""
        # Generate deterministic pseudo-random data
        np.random.seed(42)
        n = 100
        dates = pd.date_range(start='2025-01-01', periods=n, freq='D')
        
        # Generate price data with some trend and noise
        trend = np.linspace(100, 110, n)
        noise = np.random.normal(0, 2, n)
        close = trend + noise
        
        # Simulate OHLC with some range
        high = close + np.abs(np.random.normal(1, 0.5, n))
        low = close - np.abs(np.random.normal(1, 0.5, n))
        open_price = low + (high - low) * np.random.uniform(0.3, 0.7, n)
        
        # Adjust to ensure high >= close >= low, high >= open >= low
        high = np.maximum(high, close)
        high = np.maximum(high, open_price)
        low = np.minimum(low, close)
        low = np.minimum(low, open_price)
        
        volume = np.random.randint(1000000, 5000000, n)
        
        df = pd.DataFrame({
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        }, index=dates)
        return df

    # ==================== Trend Indicators Tests ====================

    def test_sma(self, sample_ohlcv_df):
        """Test Simple Moving Average calculation."""
        df = sample_ohlcv_df
        
        # Calculate using IndicatorService
        result = IndicatorService.sma(df, length=10)
        
        # Calculate using pandas-ta directly for comparison
        expected = ta.sma(close=df['close'], length=10)
        
        # Compare results (allow small floating point differences)
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_ema(self, sample_ohlcv_df):
        """Test Exponential Moving Average calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.ema(df, length=10)
        expected = ta.ema(close=df['close'], length=10)
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_wma(self, sample_ohlcv_df):
        """Test Weighted Moving Average calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.wma(df, length=10)
        expected = ta.wma(close=df['close'], length=10)
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_macd(self, sample_ohlcv_df):
        """Test MACD calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.macd(df, fast=12, slow=26, signal=9)
        expected = ta.macd(close=df['close'], fast=12, slow=26, signal=9)
        
        # MACD returns DataFrame with multiple columns
        pd.testing.assert_frame_equal(result, expected)
    
    def test_bollinger_bands(self, sample_ohlcv_df):
        """Test Bollinger Bands calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.bollinger_bands(df, length=20, std=2.0)
        expected = ta.bbands(close=df['close'], length=20, std=2.0)
        
        pd.testing.assert_frame_equal(result, expected)
    
    # ==================== Momentum Indicators Tests ====================

    def test_rsi(self, sample_ohlcv_df):
        """Test Relative Strength Index calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.rsi(df, length=14)
        expected = ta.rsi(close=df['close'], length=14)
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_kdj(self, sample_ohlcv_df):
        """Test KDJ calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.kdj(df, length=14, signal=3, smooth=3)
        
        # Calculate expected using pandas-ta directly
        expected = ta.stoch(
            high=df['high'], 
            low=df['low'], 
            close=df['close'],
            k=14,
            d=3,
            smooth_k=3
        )
        # Add J column for comparison
        if expected is not None and not expected.empty:
            k_col = expected.columns[0]
            d_col = expected.columns[1]
            expected['KDJ_J'] = 3 * expected[k_col] - 2 * expected[d_col]
        
        pd.testing.assert_frame_equal(result, expected)
    
    def test_stochastic(self, sample_ohlcv_df):
        """Test Stochastic Oscillator calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.stochastic(df, k=14, d=3, smooth_k=3)
        expected = ta.stoch(
            high=df['high'], 
            low=df['low'], 
            close=df['close'],
            k=14,
            d=3,
            smooth_k=3
        )
        
        pd.testing.assert_frame_equal(result, expected)
    
    def test_cci(self, sample_ohlcv_df):
        """Test Commodity Channel Index calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.cci(df, length=20)
        expected = ta.cci(high=df['high'], low=df['low'], close=df['close'], length=20)
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_roc(self, sample_ohlcv_df):
        """Test Rate of Change calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.roc(df, length=10)
        expected = ta.roc(close=df['close'], length=10)
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    # ==================== Volume Indicators Tests ====================

    def test_volume(self, sample_ohlcv_df):
        """Test volume indicator."""
        df = sample_ohlcv_df
        
        result = IndicatorService.volume(df)
        expected = pd.DataFrame({'volume': df['volume']})
        
        pd.testing.assert_frame_equal(result, expected)
    
    def test_obv(self, sample_ohlcv_df):
        """Test On-Balance Volume calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.obv(df)
        expected = ta.obv(close=df['close'], volume=df['volume'])
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_ad(self, sample_ohlcv_df):
        """Test Accumulation/Distribution Line calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.ad(df)
        expected = ta.ad(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'])
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_adx(self, sample_ohlcv_df):
        """Test Average Directional Index calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.adx(df, length=14)
        expected = ta.adx(high=df['high'], low=df['low'], close=df['close'], length=14)
        
        pd.testing.assert_frame_equal(result, expected)
    
    # ==================== Volatility Indicators Tests ====================

    def test_atr(self, sample_ohlcv_df):
        """Test Average True Range calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.atr(df, length=14)
        expected = ta.atr(high=df['high'], low=df['low'], close=df['close'], length=14)
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_donchian(self, sample_ohlcv_df):
        """Test Donchian Channels calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.donchian(df, lower_length=20, upper_length=20)
        expected = ta.donchian(
            high=df['high'], 
            low=df['low'], 
            lower_length=20,
            upper_length=20
        )
        
        pd.testing.assert_frame_equal(result, expected)
    
    # ==================== Additional Indicators Tests ====================

    def test_tema(self, sample_ohlcv_df):
        """Test Triple Exponential Moving Average calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.tema(df, length=10)
        expected = ta.tema(close=df['close'], length=10)
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_kama(self, sample_ohlcv_df):
        """Test Kaufman's Adaptive Moving Average calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.kama(df, length=10)
        expected = ta.kama(close=df['close'], length=10)
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_mama(self, sample_ohlcv_df):
        """Test MESA Adaptive Moving Average calculation."""
        # Skip if mama indicator is not available in pandas-ta-classic
        if not hasattr(ta, 'mama'):
            pytest.skip("mama indicator not available in pandas-ta-classic")
        
        df = sample_ohlcv_df
        
        result = IndicatorService.mama(df)
        expected = ta.mama(close=df['close'])
        
        pd.testing.assert_frame_equal(result, expected)
    
    def test_vwap(self, sample_ohlcv_df):
        """Test Volume Weighted Average Price calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.vwap(df)
        expected = ta.vwap(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'])
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_rvi(self, sample_ohlcv_df):
        """Test Relative Vigor Index calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.rvi(df, length=14)
        expected = ta.rvi(close=df['close'], length=14)
        
        # Handle different return types
        if isinstance(result, pd.Series) and isinstance(expected, pd.Series):
            pd.testing.assert_series_equal(result, expected, check_names=False)
        elif isinstance(result, pd.DataFrame) and isinstance(expected, pd.DataFrame):
            pd.testing.assert_frame_equal(result, expected)
        else:
            # Convert Series to DataFrame for comparison if needed
            if isinstance(result, pd.Series) and isinstance(expected, pd.DataFrame):
                result_df = result.to_frame()
                # Check column names
                if expected.shape[1] == 1:
                    pd.testing.assert_frame_equal(result_df, expected, check_names=False)
                else:
                    # This shouldn't happen
                    raise AssertionError(f"Type mismatch: result Series, expected DataFrame with {expected.shape[1]} columns")
            else:
                raise AssertionError(f"Type mismatch: result {type(result)}, expected {type(expected)}")
    
    def test_trix(self, sample_ohlcv_df):
        """Test TRIX calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.trix(df, length=15)
        expected = ta.trix(close=df['close'], length=15)
        
        # Handle different return types
        if isinstance(result, pd.Series) and isinstance(expected, pd.Series):
            pd.testing.assert_series_equal(result, expected, check_names=False)
        elif isinstance(result, pd.DataFrame) and isinstance(expected, pd.DataFrame):
            pd.testing.assert_frame_equal(result, expected)
        else:
            # Convert if one is Series and other is DataFrame
            if isinstance(result, pd.Series) and isinstance(expected, pd.DataFrame):
                result_df = result.to_frame()
                if expected.shape[1] == 1:
                    pd.testing.assert_frame_equal(result_df, expected, check_names=False)
                else:
                    raise AssertionError(f"Type mismatch: result Series, expected DataFrame with {expected.shape[1]} columns")
            elif isinstance(result, pd.DataFrame) and isinstance(expected, pd.Series):
                expected_df = expected.to_frame()
                if result.shape[1] == 1:
                    pd.testing.assert_frame_equal(result, expected_df, check_names=False)
                else:
                    raise AssertionError(f"Type mismatch: result DataFrame with {result.shape[1]} columns, expected Series")
            else:
                raise AssertionError(f"Type mismatch: result {type(result)}, expected {type(expected)}")
    
    def test_ppo(self, sample_ohlcv_df):
        """Test Percentage Price Oscillator calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.ppo(df, fast=12, slow=26, signal=9)
        expected = ta.ppo(close=df['close'], fast=12, slow=26, signal=9)
        
        pd.testing.assert_frame_equal(result, expected)
    
    def test_cmo(self, sample_ohlcv_df):
        """Test Chande Momentum Oscillator calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.cmo(df, length=14)
        expected = ta.cmo(close=df['close'], length=14)
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_ultosc(self, sample_ohlcv_df):
        """Test Ultimate Oscillator calculation."""
        # Skip if ultosc indicator is not available in pandas-ta-classic
        if not hasattr(ta, 'ultosc'):
            pytest.skip("ultosc indicator not available in pandas-ta-classic")
        
        df = sample_ohlcv_df
        
        result = IndicatorService.ultosc(df, fast=7, medium=14, slow=28)
        expected = ta.ultosc(high=df['high'], low=df['low'], close=df['close'], 
                           fast=7, medium=14, slow=28)
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_willr(self, sample_ohlcv_df):
        """Test Williams %R calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.willr(df, length=14)
        expected = ta.willr(high=df['high'], low=df['low'], close=df['close'], length=14)
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_ao(self, sample_ohlcv_df):
        """Test Awesome Oscillator calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.ao(df, fast=5, slow=34)
        expected = ta.ao(high=df['high'], low=df['low'], fast=5, slow=34)
        
        pd.testing.assert_series_equal(result, expected, check_names=False)
    
    def test_kst(self, sample_ohlcv_df):
        """Test Know Sure Thing calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.kst(df)
        expected = ta.kst(close=df['close'])
        
        pd.testing.assert_frame_equal(result, expected)
    
    def test_ichimoku(self, sample_ohlcv_df):
        """Test Ichimoku Kinko Hyo calculation."""
        df = sample_ohlcv_df
        
        result = IndicatorService.ichimoku(df, tenkan=9, kijun=26, senkou=52, offset=26)
        expected = ta.ichimoku(
            high=df['high'], 
            low=df['low'], 
            close=df['close'],
            tenkan=9,
            kijun=26,
            senkou=52,
            offset=26
        )
        
        # ichimoku returns a tuple of DataFrames, compare each component
        if isinstance(result, tuple) and isinstance(expected, tuple):
            assert len(result) == len(expected), f"Tuple length mismatch: {len(result)} vs {len(expected)}"
            for i, (res_item, exp_item) in enumerate(zip(result, expected)):
                if isinstance(res_item, pd.DataFrame) and isinstance(exp_item, pd.DataFrame):
                    pd.testing.assert_frame_equal(res_item, exp_item)
                elif isinstance(res_item, pd.Series) and isinstance(exp_item, pd.Series):
                    pd.testing.assert_series_equal(res_item, exp_item, check_names=False)
                else:
                    # Fallback to equality check
                    assert res_item.equals(exp_item), f"Ichimoku component {i} mismatch"
        else:
            # If not tuples, compare directly
            if isinstance(result, pd.DataFrame) and isinstance(expected, pd.DataFrame):
                pd.testing.assert_frame_equal(result, expected)
            elif isinstance(result, pd.Series) and isinstance(expected, pd.Series):
                pd.testing.assert_series_equal(result, expected, check_names=False)
            else:
                raise AssertionError(f"Unexpected return types: result {type(result)}, expected {type(expected)}")
    
    # ==================== Edge Cases and Validation Tests ====================

    def test_validate_dataframe_missing_columns(self):
        """Test DataFrame validation with missing columns."""
        df = pd.DataFrame({'close': [1, 2, 3]})
        
        with pytest.raises(ValueError, match="missing required columns"):
            IndicatorService.sma(df, length=10)
    
    def test_validate_dataframe_with_extra_columns(self):
        """Test DataFrame validation with extra columns (should pass)."""
        df = pd.DataFrame({
            'open': [1, 2, 3],
            'high': [1.5, 2.5, 3.5],
            'low': [0.5, 1.5, 2.5],
            'close': [1.2, 2.2, 3.2],
            'volume': [1000, 2000, 3000],
            'extra': [0, 0, 0]
        })
        
        # Should not raise exception
        result = IndicatorService.sma(df, length=2)
        assert len(result) == 3
    
    def test_volume_missing_column(self):
        """Test volume indicator with missing volume column."""
        df = pd.DataFrame({
            'open': [1, 2, 3],
            'high': [1.5, 2.5, 3.5],
            'low': [0.5, 1.5, 2.5],
            'close': [1.2, 2.2, 3.2]
        })
        
        with pytest.raises(ValueError, match="missing 'volume' column"):
            IndicatorService.volume(df)
    
    def test_obv_missing_volume(self):
        """Test OBV calculation with missing volume column."""
        df = pd.DataFrame({
            'open': [1, 2, 3],
            'high': [1.5, 2.5, 3.5],
            'low': [0.5, 1.5, 2.5],
            'close': [1.2, 2.2, 3.2]
        })
        
        with pytest.raises(ValueError, match="missing 'volume' column"):
            IndicatorService.obv(df)
    
    def test_different_source_column(self):
        """Test indicator calculation with different source column."""
        df = pd.DataFrame({
            'open': [1, 2, 3, 4, 5],
            'high': [1.5, 2.5, 3.5, 4.5, 5.5],
            'low': [0.5, 1.5, 2.5, 3.5, 4.5],
            'close': [1.2, 2.2, 3.2, 4.2, 5.2]
        })
        
        # Test SMA with 'open' as source
        result = IndicatorService.sma(df, length=3, source='open')
        expected = ta.sma(close=df['open'], length=3)
        
        pd.testing.assert_series_equal(result, expected, check_names=False)


class TestCustomIndicator:
    """Test CustomIndicator class."""
    
    def test_custom_indicator_creation_valid(self):
        """Test creating a valid custom indicator."""
        indicator = CustomIndicator(
            name="custom_ma_diff",
            expression="(sma_10 - sma_20) / sma_10 * 100",
            description="Difference between two SMAs as percentage"
        )
        
        assert indicator.name == "custom_ma_diff"
        assert indicator.expression == "(sma_10 - sma_20) / sma_10 * 100"
        assert indicator.description == "Difference between two SMAs as percentage"
    
    def test_custom_indicator_creation_invalid_syntax(self):
        """Test creating a custom indicator with invalid syntax."""
        with pytest.raises(SyntaxError):
            CustomIndicator(
                name="invalid",
                expression="sma_10 - sma_20 /",  # Invalid syntax
                description="Invalid expression"
            )
    
    def test_custom_indicator_calculation(self):
        """Test custom indicator calculation."""
        indicator = CustomIndicator(
            name="simple_avg",
            expression="(value1 + value2) / 2"
        )
        
        data = {'value1': 10, 'value2': 20}
        result = indicator.calculate(data)
        
        assert result == 15.0
    
    def test_custom_indicator_with_builtins(self):
        """Test custom indicator using allowed built-in functions."""
        indicator = CustomIndicator(
            name="range_ratio",
            expression="max(values) - min(values)"
        )
        
        data = {'values': [1, 5, 3, 8, 2]}
        result = indicator.calculate(data)
        
        assert result == 7  # max=8, min=1
    
    def test_custom_indicator_uncompiled_error(self):
        """Test error when calculating uncompiled indicator."""
        # Create indicator but simulate compilation failure
        indicator = CustomIndicator(
            name="test",
            expression="x + y"
        )
        # Manually set _compiled to None to simulate compilation failure
        indicator._compiled = None
        
        with pytest.raises(RuntimeError, match="has not been compiled"):
            indicator.calculate({'x': 1, 'y': 2})


class TestCustomIndicatorManager:
    """Test CustomIndicatorManager class."""
    
    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset the global indicator manager before each test."""
        # Clear any existing indicators
        global indicator_manager
        # We can't directly clear the manager's internal dict, 
        # so we'll create a new one for testing
        # Instead, we'll test with a fresh instance
        pass
    
    def test_register_and_get_indicator(self):
        """Test registering and retrieving an indicator."""
        manager = CustomIndicatorManager()
        indicator = CustomIndicator("test", "x + y")
        
        manager.register(indicator)
        retrieved = manager.get("test")
        
        assert retrieved is indicator
    
    def test_register_overwrite(self):
        """Test overwriting an existing indicator."""
        manager = CustomIndicatorManager()
        indicator1 = CustomIndicator("test", "x + y")
        indicator2 = CustomIndicator("test", "x * y")
        
        manager.register(indicator1)
        # Should not raise exception
        manager.register(indicator2)
        
        retrieved = manager.get("test")
        assert retrieved is indicator2
    
    def test_unregister_existing(self):
        """Test unregistering an existing indicator."""
        manager = CustomIndicatorManager()
        indicator = CustomIndicator("test", "x + y")
        
        manager.register(indicator)
        result = manager.unregister("test")
        
        assert result is True
        assert manager.get("test") is None
    
    def test_unregister_nonexistent(self):
        """Test unregistering a nonexistent indicator."""
        manager = CustomIndicatorManager()
        
        result = manager.unregister("nonexistent")
        
        assert result is False
    
    def test_list_indicators(self):
        """Test listing all registered indicators."""
        manager = CustomIndicatorManager()
        indicator1 = CustomIndicator("ind1", "x + y")
        indicator2 = CustomIndicator("ind2", "x * y")
        
        manager.register(indicator1)
        manager.register(indicator2)
        
        indicators = manager.list_indicators()
        
        assert len(indicators) == 2
        assert indicators["ind1"] is indicator1
        assert indicators["ind2"] is indicator2
    
    def test_global_manager_instance(self):
        """Test the global indicator manager instance."""
        # The global instance should exist
        assert isinstance(indicator_manager, CustomIndicatorManager)
        
        # Test that we can use it
        indicator = CustomIndicator("global_test", "close * 2")
        indicator_manager.register(indicator)
        
        retrieved = indicator_manager.get("global_test")
        assert retrieved is indicator
        
        # Clean up
        indicator_manager.unregister("global_test")