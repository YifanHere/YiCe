"""Unit tests for data providers and services."""
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from typing import List, Dict, Any
import pytest
import pandas as pd
import numpy as np

# Import modules to test
from app.core.providers.tushare_provider import TushareProvider
from app.services.kline_service import KlineDataService, RateLimiter
from app.services.fundamental_service import FundamentalDataService
from app.services.macro_service import MacroDataService
from app.models.data_models import KlineData, FundamentalData
from app.core.exceptions import DataProviderError, DataServiceError


class TestTushareProvider:
    """Test TushareProvider class."""
    
    @pytest.fixture
    def mock_tushare(self, mocker):
        """Mock tushare module."""
        mock_ts = mocker.patch('app.core.providers.tushare_provider.ts')
        mock_pro = MagicMock()
        mock_ts.pro_api.return_value = mock_pro
        return mock_ts, mock_pro
    
    @pytest.fixture
    def sample_kline_df(self):
        """Create sample kline DataFrame."""
        data = {
            'trade_date': ['20250101', '20250102'],
            'open': [10.0, 10.5],
            'high': [10.8, 11.0],
            'low': [9.8, 10.2],
            'close': [10.2, 10.8],
            'vol': [1000000, 1200000],
            'amount': [10000000, 13000000],
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def sample_daily_basic_df(self):
        """Create sample daily basic DataFrame."""
        data = {
            'ts_code': ['000001.SZ'],
            'trade_date': ['20250102'],
            'total_mv': [1000000000.0],
            'circ_mv': [800000000.0],
            'total_share': [1000000000.0],
            'float_share': [800000000.0],
            'pe': [15.0],
            'pe_ttm': [14.5],
            'pb': [1.5],
            'ps': [2.0],
            'ps_ttm': [1.8],
            'dv_ratio': [2.5],
            'dv_ttm': [2.4],
            'turnover_rate': [1.2],
            'turnover_rate_f': [1.0],
            'volume_ratio': [1.1],
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def sample_stock_basic_df(self):
        """Create sample stock basic DataFrame."""
        data = {
            'ts_code': ['000001.SZ'],
            'name': ['平安银行'],
            'area': ['深圳'],
            'industry': ['银行'],
            'market': ['主板'],
            'list_date': ['19910403'],
            'fullname': ['平安银行股份有限公司'],
            'enname': ['Ping An Bank'],
            'exchange': ['SZSE'],
            'curr_type': ['CNY'],
        }
        return pd.DataFrame(data)
    
    def test_init_with_token(self, mocker):
        """Test initialization with token."""
        mock_ts = mocker.patch('app.core.providers.tushare_provider.ts')
        mock_pro = MagicMock()
        mock_ts.pro_api.return_value = mock_pro
        
        provider = TushareProvider(token="test_token")
        
        assert provider.token == "test_token"
        mock_ts.set_token.assert_called_once_with("test_token")
        mock_ts.pro_api.assert_called_once()
        assert provider.pro == mock_pro
    
    def test_init_without_token(self, mocker):
        """Test initialization without token (should use settings)."""
        mock_ts = mocker.patch('app.core.providers.tushare_provider.ts')
        mock_settings = mocker.patch('app.core.providers.tushare_provider.settings')
        mock_settings.TUSHARE_TOKEN = "env_token"
        mock_pro = MagicMock()
        mock_ts.pro_api.return_value = mock_pro
        
        provider = TushareProvider()
        
        assert provider.token == "env_token"
        mock_ts.set_token.assert_called_once_with("env_token")
        mock_ts.pro_api.assert_called_once()
    
    def test_init_missing_token(self, mocker):
        """Test initialization with missing token raises ValueError."""
        mock_settings = mocker.patch('app.core.providers.tushare_provider.settings')
        mock_settings.TUSHARE_TOKEN = None
        
        with pytest.raises(ValueError, match="Tushare token must be provided"):
            TushareProvider()
    
    @pytest.mark.asyncio
    async def test_get_kline_success(self, mocker, sample_kline_df):
        """Test successful kline data retrieval."""
        mock_ts = mocker.patch('app.core.providers.tushare_provider.ts')
        mock_pro = MagicMock()
        mock_ts.pro_api.return_value = mock_pro
        mock_pro.pro_bar.return_value = sample_kline_df
        
        # Mock DataConverter
        mock_converter = mocker.patch('app.core.providers.tushare_provider.DataConverter')
        expected_kline_data = [
            KlineData(
                symbol="000001.SZ",
                timestamp=datetime.now(),
                open=10.0,
                high=10.8,
                low=9.8,
                close=10.2,
                volume=1000000,
                amount=10000000.0
            )
        ]
        mock_converter.tushare_kline_to_kline_data.return_value = expected_kline_data
        
        provider = TushareProvider(token="test_token")
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 1, 2)
        
        result = await provider.get_kline(
            symbol="000001.SZ",
            start_date=start_date,
            end_date=end_date,
            period="daily"
        )
        
        mock_pro.pro_bar.assert_called_once_with(
            ts_code="000001.SZ",
            asset="E",
            freq="D",
            start_date="20250101",
            end_date="20250102",
            adj="qfq"
        )
        mock_converter.tushare_kline_to_kline_data.assert_called_once_with(sample_kline_df)
        assert result == expected_kline_data
    
    @pytest.mark.asyncio
    async def test_get_kline_empty_data(self, mocker):
        """Test kline retrieval with empty data."""
        mock_ts = mocker.patch('app.core.providers.tushare_provider.ts')
        mock_pro = MagicMock()
        mock_ts.pro_api.return_value = mock_pro
        mock_pro.pro_bar.return_value = None
        
        provider = TushareProvider(token="test_token")
        
        result = await provider.get_kline(symbol="000001.SZ")
        
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_kline_exception(self, mocker):
        """Test kline retrieval with exception."""
        mock_ts = mocker.patch('app.core.providers.tushare_provider.ts')
        mock_pro = MagicMock()
        mock_ts.pro_api.return_value = mock_pro
        mock_pro.pro_bar.side_effect = Exception("API Error")
        
        provider = TushareProvider(token="test_token")
        
        with pytest.raises(DataProviderError) as exc_info:
            await provider.get_kline(symbol="000001.SZ")
        
        assert "API Error" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_get_fundamental_success(self, mocker, sample_daily_basic_df, sample_stock_basic_df):
        """Test successful fundamental data retrieval."""
        mock_ts = mocker.patch('app.core.providers.tushare_provider.ts')
        mock_pro = MagicMock()
        mock_ts.pro_api.return_value = mock_pro
        
        # Mock API calls
        today_str = datetime.now().strftime("%Y%m%d")
        mock_pro.daily_basic.return_value = sample_daily_basic_df
        mock_pro.stock_basic.return_value = sample_stock_basic_df
        
        # Mock DataConverter
        mock_converter = mocker.patch('app.core.providers.tushare_provider.DataConverter')
        expected_fundamental = FundamentalData(symbol="000001.SZ", name="平安银行")
        mock_converter.tushare_daily_basic_to_fundamental_data.return_value = expected_fundamental
        
        provider = TushareProvider(token="test_token")
        
        result = await provider.get_fundamental(symbol="000001.SZ")
        
        mock_pro.daily_basic.assert_called_once_with(ts_code="000001.SZ", trade_date=today_str)
        mock_pro.stock_basic.assert_called_once_with(ts_code="000001.SZ")
        mock_converter.tushare_daily_basic_to_fundamental_data.assert_called_once()
        assert result == expected_fundamental
    
    @pytest.mark.asyncio
    async def test_get_fundamental_fallback(self, mocker, sample_daily_basic_df):
        """Test fundamental retrieval with fallback to latest data."""
        mock_ts = mocker.patch('app.core.providers.tushare_provider.ts')
        mock_pro = MagicMock()
        mock_ts.pro_api.return_value = mock_pro
        
        # First call returns empty, second returns data
        mock_pro.daily_basic.side_effect = [pd.DataFrame(), sample_daily_basic_df]
        mock_pro.stock_basic.return_value = pd.DataFrame({'name': ['Test']})
        
        mock_converter = mocker.patch('app.core.providers.tushare_provider.DataConverter')
        mock_converter.tushare_daily_basic_to_fundamental_data.return_value = FundamentalData(
            symbol="000001.SZ", name="Test"
        )
        
        provider = TushareProvider(token="test_token")
        
        result = await provider.get_fundamental(symbol="000001.SZ")
        
        # Should have called daily_basic twice
        assert mock_pro.daily_basic.call_count == 2
        mock_pro.daily_basic.assert_called_with(ts_code="000001.SZ", limit=1)
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_get_fundamental_no_data(self, mocker):
        """Test fundamental retrieval with no data."""
        mock_ts = mocker.patch('app.core.providers.tushare_provider.ts')
        mock_pro = MagicMock()
        mock_ts.pro_api.return_value = mock_pro
        mock_pro.daily_basic.return_value = pd.DataFrame()
        mock_pro.stock_basic.return_value = pd.DataFrame()
        
        provider = TushareProvider(token="test_token")
        
        result = await provider.get_fundamental(symbol="000001.SZ")
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_search_symbol_success(self, mocker):
        """Test successful symbol search."""
        mock_ts = mocker.patch('app.core.providers.tushare_provider.ts')
        mock_pro = MagicMock()
        mock_ts.pro_api.return_value = mock_pro
        
        sample_df = pd.DataFrame({
            'ts_code': ['000001.SZ', '000002.SZ', '600000.SH'],
            'name': ['平安银行', '万科A', '浦发银行']
        })
        mock_pro.stock_basic.return_value = sample_df
        
        provider = TushareProvider(token="test_token")
        
        # Search by symbol
        result = await provider.search_symbol("000001")
        assert result == ['000001.SZ']
        
        # Search by name
        result = await provider.search_symbol("平安")
        assert result == ['000001.SZ']
        
        # Search by partial name
        result = await provider.search_symbol("银行")
        assert set(result) == {'000001.SZ', '600000.SH'}
    
    @pytest.mark.asyncio
    async def test_search_symbol_empty(self, mocker):
        """Test symbol search with empty result."""
        mock_ts = mocker.patch('app.core.providers.tushare_provider.ts')
        mock_pro = MagicMock()
        mock_ts.pro_api.return_value = mock_pro
        mock_pro.stock_basic.return_value = pd.DataFrame()
        
        provider = TushareProvider(token="test_token")
        
        result = await provider.search_symbol("nonexistent")
        
        assert result == []
    
    @pytest.mark.asyncio
    async def test_search_symbol_exception(self, mocker):
        """Test symbol search with exception."""
        mock_ts = mocker.patch('app.core.providers.tushare_provider.ts')
        mock_pro = MagicMock()
        mock_ts.pro_api.return_value = mock_pro
        mock_pro.stock_basic.side_effect = Exception("API Error")
        
        provider = TushareProvider(token="test_token")
        
        with pytest.raises(DataProviderError) as exc_info:
            await provider.search_symbol("test")
        
        assert "API Error" in str(exc_info.value)


class TestKlineDataService:
    """Test KlineDataService class."""
    
    @pytest.fixture
    def mock_provider(self, mocker):
        """Mock data provider."""
        mock_provider = AsyncMock()
        mock_factory = mocker.patch('app.services.kline_service.DataSourceFactory')
        mock_factory.get_provider.return_value = mock_provider
        return mock_provider
    
    @pytest.fixture
    def sample_kline_data(self):
        """Create sample kline data."""
        return [
            KlineData(
                symbol="000001.SZ",
                timestamp=datetime(2025, 1, 1),
                open=10.0,
                high=10.8,
                low=9.8,
                close=10.2,
                volume=1000000,
                amount=10000000.0
            ),
            KlineData(
                symbol="000001.SZ",
                timestamp=datetime(2025, 1, 2),
                open=10.5,
                high=11.0,
                low=10.2,
                close=10.8,
                volume=1200000,
                amount=13000000.0
            )
        ]
    
    @pytest.mark.asyncio
    async def test_init_success(self, mocker):
        """Test successful initialization."""
        mock_provider = AsyncMock()
        mock_factory = mocker.patch('app.services.kline_service.DataSourceFactory')
        mock_factory.get_provider.return_value = mock_provider
        
        service = KlineDataService()
        
        assert service.provider == mock_provider
        assert service.rate_limiter is not None
    
    @pytest.mark.asyncio
    async def test_init_failure(self, mocker):
        """Test initialization failure."""
        mock_factory = mocker.patch('app.services.kline_service.DataSourceFactory')
        mock_factory.get_provider.return_value = None
        
        with pytest.raises(ValueError, match="Failed to initialize Tushare provider"):
            KlineDataService()
    
    @pytest.mark.asyncio
    async def test_get_daily_kline(self, mock_provider, sample_kline_data):
        """Test get_daily_kline method."""
        mock_provider.get_kline.return_value = sample_kline_data
        
        service = KlineDataService()
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 1, 2)
        
        result = await service.get_daily_kline(
            symbol="000001.SZ",
            start_date=start_date,
            end_date=end_date
        )
        
        mock_provider.get_kline.assert_called_once_with(
            "000001.SZ",
            start_date,
            end_date,
            period="daily"
        )
        assert result == sample_kline_data
    
    @pytest.mark.asyncio
    async def test_get_weekly_kline(self, mock_provider, sample_kline_data):
        """Test get_weekly_kline method."""
        mock_provider.get_kline.return_value = sample_kline_data
        
        service = KlineDataService()
        
        result = await service.get_weekly_kline(symbol="000001.SZ")
        
        mock_provider.get_kline.assert_called_once_with(
            "000001.SZ",
            None,
            None,
            period="weekly"
        )
        assert result == sample_kline_data
    
    @pytest.mark.asyncio
    async def test_get_monthly_kline(self, mock_provider, sample_kline_data):
        """Test get_monthly_kline method."""
        mock_provider.get_kline.return_value = sample_kline_data
        
        service = KlineDataService()
        
        result = await service.get_monthly_kline(symbol="000001.SZ")
        
        mock_provider.get_kline.assert_called_once_with(
            "000001.SZ",
            None,
            None,
            period="monthly"
        )
        assert result == sample_kline_data
    
    @pytest.mark.asyncio
    async def test_rate_limiter_acquire(self, mocker):
        """Test rate limiter acquire method."""
        rate_limiter = RateLimiter(max_calls=2, period=0.1)
        
        # First two calls should pass quickly
        start = datetime.now()
        await rate_limiter.acquire()
        await rate_limiter.acquire()
        
        # Third call should wait
        await rate_limiter.acquire()
        elapsed = (datetime.now() - start).total_seconds()
        
        # Should have waited at least some small amount
        assert elapsed >= 0.05


class TestFundamentalDataService:
    """Test FundamentalDataService class."""
    
    @pytest.fixture
    def mock_provider(self, mocker):
        """Mock TushareProvider."""
        # Create a mock provider with pro attribute
        mock_provider_instance = MagicMock()
        mock_provider_instance.pro = MagicMock()
        # Mock DataSourceFactory to return the mock provider instance
        mock_factory = mocker.patch('app.services.fundamental_service.DataSourceFactory')
        mock_factory.get_provider.return_value = mock_provider_instance
        # Mock _init_provider to set provider directly
        mocker.patch(
            'app.services.fundamental_service.FundamentalDataService._init_provider',
            lambda self: setattr(self, 'provider', mock_provider_instance)
        )
        return mock_provider_instance
    
    @pytest.fixture
    def sample_financial_df(self):
        """Create sample financial DataFrame."""
        data = {
            'ts_code': ['000001.SZ', '000001.SZ'],
            'end_date': ['20241231', '20240930'],
            'total_assets': [1000000000.0, 950000000.0],
            'total_liab': [800000000.0, 750000000.0],
            'total_equity': [200000000.0, 200000000.0],
            'revenue': [50000000.0, 45000000.0],
            'net_profit': [10000000.0, 9000000.0],
        }
        return pd.DataFrame(data)
    
    @pytest.mark.asyncio
    async def test_init_success(self, mock_provider):
        """Test successful initialization."""
        service = FundamentalDataService()
        assert service.provider == mock_provider
    
    @pytest.mark.asyncio
    async def test_get_financial_report_balance(self, mock_provider, sample_financial_df):
        """Test get_financial_report with balance sheet."""
        mock_provider.pro.balancesheet.return_value = sample_financial_df
        
        service = FundamentalDataService()
        
        result = await service.get_financial_report(
            symbol="000001.SZ",
            report_type="balance"
        )
        
        mock_provider.pro.balancesheet.assert_called_once_with(ts_code="000001.SZ", limit=5)
        assert len(result) == 2
        assert result[0]['end_date'] == '20241231'
        assert result[0]['report_date'] == '20241231'
    
    @pytest.mark.asyncio
    async def test_get_financial_report_income(self, mock_provider, sample_financial_df):
        """Test get_financial_report with income statement."""
        mock_provider.pro.income.return_value = sample_financial_df
        
        service = FundamentalDataService()
        
        result = await service.get_financial_report(
            symbol="000001.SZ",
            report_type="income",
            period="20241231"
        )
        
        mock_provider.pro.income.assert_called_once_with(ts_code="000001.SZ", end_date="20241231")
        assert len(result) == 2
    
    @pytest.mark.asyncio
    async def test_get_financial_report_cashflow(self, mock_provider):
        """Test get_financial_report with cash flow."""
        mock_provider.pro.cashflow.return_value = pd.DataFrame({'end_date': ['20241231']})
        
        service = FundamentalDataService()
        
        result = await service.get_financial_report(
            symbol="000001.SZ",
            report_type="cashflow"
        )
        
        mock_provider.pro.cashflow.assert_called_once_with(ts_code="000001.SZ", limit=5)
        assert result[0]['end_date'] == '20241231'
    
    @pytest.mark.asyncio
    async def test_get_financial_report_invalid_type(self, mock_provider):
        """Test get_financial_report with invalid report type."""
        service = FundamentalDataService()
        
        result = await service.get_financial_report(
            symbol="000001.SZ",
            report_type="invalid"
        )
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_financial_report_no_data(self, mock_provider):
        """Test get_financial_report with no data."""
        mock_provider.pro.balancesheet.return_value = pd.DataFrame()
        
        service = FundamentalDataService()
        
        result = await service.get_financial_report(
            symbol="000001.SZ",
            report_type="balance"
        )
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_company_info_success(self, mock_provider):
        """Test get_company_info success."""
        sample_df = pd.DataFrame({
            'ts_code': ['000001.SZ'],
            'name': ['平安银行'],
            'area': ['深圳'],
            'industry': ['银行'],
            'market': ['主板'],
            'list_date': ['19910403'],
            'fullname': ['平安银行股份有限公司'],
            'enname': ['Ping An Bank'],
            'exchange': ['SZSE'],
            'curr_type': ['CNY'],
        })
        mock_provider.pro.stock_basic.return_value = sample_df
        
        service = FundamentalDataService()
        
        result = await service.get_company_info(symbol="000001.SZ")
        
        mock_provider.pro.stock_basic.assert_called_once_with(ts_code="000001.SZ")
        assert result['symbol'] == '000001.SZ'
        assert result['name'] == '平安银行'
        assert result['industry'] == '银行'
    
    @pytest.mark.asyncio
    async def test_get_company_info_no_data(self, mock_provider):
        """Test get_company_info with no data."""
        mock_provider.pro.stock_basic.return_value = pd.DataFrame()
        
        service = FundamentalDataService()
        
        result = await service.get_company_info(symbol="000001.SZ")
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_industry_classification_all(self, mock_provider):
        """Test get_industry_classification without symbol."""
        sample_df = pd.DataFrame({
            'index_code': ['801010', '801020'],
            'industry_name': ['银行', '证券'],
            'level': ['L1', 'L1'],
            'src': ['SW', 'SW']
        })
        mock_provider.pro.index_classify.return_value = sample_df
        
        service = FundamentalDataService()
        
        result = await service.get_industry_classification(industry_level="L1")
        
        mock_provider.pro.index_classify.assert_called_once_with(level="L1", src="SW")
        assert len(result) == 2
        assert result[0]['industry_name'] == '银行'
    
    @pytest.mark.asyncio
    async def test_get_industry_classification_for_symbol(self, mock_provider):
        """Test get_industry_classification for specific symbol."""
        industry_df = pd.DataFrame({
            'index_code': ['801010'],
            'industry_name': ['银行'],
            'level': ['L1'],
            'src': ['SW']
        })
        member_df = pd.DataFrame({
            'index_code': ['801010'],
            'con_code': ['000001.SZ']
        })
        
        mock_provider.pro.index_classify.return_value = industry_df
        mock_provider.pro.index_member.return_value = member_df
        
        service = FundamentalDataService()
        
        result = await service.get_industry_classification(
            symbol="000001.SZ",
            industry_level="L1"
        )
        
        assert len(result) == 1
        assert result[0]['industry_name'] == '银行'
    
    @pytest.mark.asyncio
    async def test_get_industry_classification_no_data(self, mock_provider):
        """Test get_industry_classification with no data."""
        mock_provider.pro.index_classify.return_value = pd.DataFrame()
        
        service = FundamentalDataService()
        
        result = await service.get_industry_classification()
        
        assert result is None


class TestMacroDataService:
    """Test MacroDataService class."""
    
    @pytest.fixture
    def mock_provider(self, mocker):
        """Mock TushareProvider."""
        mock_provider = MagicMock()
        mock_factory = mocker.patch('app.services.macro_service.DataSourceFactory')
        mock_factory.get_provider.return_value = mock_provider
        return mock_provider
    
    @pytest.fixture
    def sample_gdp_df(self):
        """Create sample GDP DataFrame."""
        data = {
            'date': ['20240101', '20240401'],
            'year': [2024, 2024],
            'quarter': [1, 2],
            'gdp': [1000000.0, 1050000.0],
            'gdp_yoy': [5.0, 5.2],
            'pi': [200000.0, 210000.0],
            'pi_yoy': [4.5, 4.7],
            'si': [400000.0, 420000.0],
            'si_yoy': [5.5, 5.7],
            'ti': [400000.0, 420000.0],
            'ti_yoy': [6.0, 6.2],
        }
        return pd.DataFrame(data)
    
    @pytest.mark.asyncio
    async def test_init_success(self, mock_provider):
        """Test successful initialization."""
        service = MacroDataService()
        assert service.provider == mock_provider
    
    @pytest.mark.asyncio
    async def test_init_failure(self, mocker):
        """Test initialization failure."""
        mock_factory = mocker.patch('app.services.macro_service.DataSourceFactory')
        mock_factory.get_provider.return_value = None
        
        with pytest.raises(ValueError, match="Tushare provider not available"):
            MacroDataService()
    
    @pytest.mark.asyncio
    async def test_get_gdp(self, mock_provider, sample_gdp_df):
        """Test get_gdp method."""
        mock_provider.pro.cn_gdp.return_value = sample_gdp_df
        
        service = MacroDataService()
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 6, 30)
        
        result = await service.get_gdp(start_date=start_date, end_date=end_date)
        
        mock_provider.pro.cn_gdp.assert_called_once_with(
            start_date="20240101",
            end_date="20240630"
        )
        assert len(result) == 2
        assert result[0]['date'] == '20240101'
        assert result[0]['gdp'] == 1000000.0
        assert result[0]['gdp_yoy'] == 5.0
        assert result[1]['quarter'] == 2
    
    @pytest.mark.asyncio
    async def test_get_gdp_no_data(self, mock_provider):
        """Test get_gdp with no data."""
        mock_provider.pro.cn_gdp.return_value = pd.DataFrame()
        
        service = MacroDataService()
        
        result = await service.get_gdp()
        
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_cpi(self, mock_provider):
        """Test get_cpi method."""
        sample_df = pd.DataFrame({
            'date': ['20240101', '20240201'],
            'month': [1, 2],
            'cpi': [102.5, 102.8],
            'cpi_nt': [102.0, 102.2],
            'cpi_t': [103.0, 103.2],
            'cpi_food': [105.0, 105.5],
            'cpi_notfood': [101.5, 101.8],
        })
        mock_provider.pro.cn_cpi.return_value = sample_df
        
        service = MacroDataService()
        
        result = await service.get_cpi()
        
        mock_provider.pro.cn_cpi.assert_called_once_with(start_date=None, end_date=None)
        assert len(result) == 2
        assert result[0]['cpi'] == 102.5
        assert result[1]['month'] == 2
    
    @pytest.mark.asyncio
    async def test_get_ppi(self, mock_provider):
        """Test get_ppi method."""
        sample_df = pd.DataFrame({
            'date': ['20240101'],
            'month': [1],
            'ppi': [98.5],
            'ppi_mp': [99.0],
            'ppi_pi': [98.0],
            'ppi_rm': [97.5],
            'ppi_ru': [96.0],
        })
        mock_provider.pro.cn_ppi.return_value = sample_df
        
        service = MacroDataService()
        
        result = await service.get_ppi()
        
        mock_provider.pro.cn_ppi.assert_called_once_with(start_date=None, end_date=None)
        assert len(result) == 1
        assert result[0]['ppi'] == 98.5
    
    @pytest.mark.asyncio
    async def test_get_interest_rate(self, mock_provider):
        """Test get_interest_rate method."""
        sample_df = pd.DataFrame({
            'date': ['20240101'],
            'on': [1.85],
            '1w': [2.05],
            '2w': [2.15],
            '1m': [2.35],
            '3m': [2.45],
            '6m': [2.55],
            '9m': [2.65],
            '1y': [2.75],
        })
        mock_provider.pro.shibor.return_value = sample_df
        
        service = MacroDataService()
        
        result = await service.get_interest_rate()
        
        mock_provider.pro.shibor.assert_called_once_with(start_date=None, end_date=None)
        assert len(result) == 1
        assert result[0]['on'] == 1.85
        assert result[0]['1y'] == 2.75
    
    @pytest.mark.asyncio
    async def test_get_money_supply(self, mock_provider):
        """Test get_money_supply method."""
        sample_df = pd.DataFrame({
            'date': ['20240101'],
            'month': [1],
            'm0': [100000.0],
            'm0_yoy': [5.0],
            'm1': [500000.0],
            'm1_yoy': [6.0],
            'm2': [2000000.0],
            'm2_yoy': [8.0],
        })
        mock_provider.pro.cn_m.return_value = sample_df
        
        service = MacroDataService()
        
        result = await service.get_money_supply()
        
        mock_provider.pro.cn_m.assert_called_once_with(start_date=None, end_date=None)
        assert len(result) == 1
        assert result[0]['m0'] == 100000.0
        assert result[0]['m2_yoy'] == 8.0
    
    @pytest.mark.asyncio
    async def test_get_macro_data_exception(self, mock_provider):
        """Test macro data retrieval with exception."""
        mock_provider.pro.cn_gdp.side_effect = Exception("API Error")
        
        service = MacroDataService()
        
        with pytest.raises(DataServiceError) as exc_info:
            await service.get_gdp()
        
        assert "API Error" in str(exc_info.value)