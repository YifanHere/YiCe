# API 使用示例

本文档提供 YiCe 数据层 API 的使用示例，包括 K线数据获取、基本面数据查询、技术指标计算和自定义指标使用。

## 快速开始

### 安装依赖
确保已安装所需依赖：
```bash
cd backend
uv pip install -r pyproject.toml
```

### 环境配置
设置 Tushare Token（必需）：
```bash
# 在 backend/.env 文件中设置
TUSHARE_TOKEN=你的Tushare Pro令牌

# Redis 配置（可选，用于缓存）
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

## 基础使用

### 1. 获取 K 线数据

#### 使用 KlineDataService
```python
import asyncio
from datetime import datetime, timedelta
from app.services.kline_service import KlineDataService

async def example_get_kline():
    # 创建服务实例
    service = KlineDataService()
    
    # 获取平安银行日K数据
    symbol = "000001.SZ"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    try:
        # 获取日K线
        daily_kline = await service.get_daily_kline(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date
        )
        
        print(f"获取到 {len(daily_kline)} 条日K数据")
        for kline in daily_kline[:3]:  # 显示前3条
            print(f"日期: {kline.timestamp.date()}, "
                  f"开盘: {kline.open:.2f}, 收盘: {kline.close:.2f}, "
                  f"成交量: {kline.volume:.0f}")
        
        # 获取周K线
        weekly_kline = await service.get_weekly_kline(symbol)
        print(f"获取到 {len(weekly_kline)} 条周K数据")
        
        # 获取月K线
        monthly_kline = await service.get_monthly_kline(symbol)
        print(f"获取到 {len(monthly_kline)} 条月K数据")
        
    except Exception as e:
        print(f"获取K线数据失败: {e}")

# 运行示例
asyncio.run(example_get_kline())
```

### 2. 获取基本面数据

#### 使用 FundamentalDataService
```python
import asyncio
from app.services.fundamental_service import FundamentalDataService

async def example_get_fundamental():
    service = FundamentalDataService()
    
    # 获取公司基本信息
    company_info = await service.get_company_info("000001.SZ")
    if company_info:
        print(f"公司名称: {company_info.get('name')}")
        print(f"上市日期: {company_info.get('list_date')}")
        print(f"所属行业: {company_info.get('industry')}")
    
    # 获取财务报表（资产负债表）
    balance_sheet = await service.get_financial_report(
        symbol="000001.SZ",
        report_type="balance"
    )
    if balance_sheet:
        print(f"获取到 {len(balance_sheet)} 条资产负债表记录")
        for record in balance_sheet[:2]:
            print(f"报告期: {record.get('end_date')}, "
                  f"总资产: {record.get('total_assets')}")
    
    # 获取行业分类
    industries = await service.get_industry_classification(industry_level="L1")
    if industries:
        print(f"获取到 {len(industries)} 个一级行业")

asyncio.run(example_get_fundamental())
```

### 3. 获取宏观数据

#### 使用 MacroDataService
```python
import asyncio
from datetime import datetime, timedelta
from app.services.macro_service import MacroDataService

async def example_get_macro():
    service = MacroDataService()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # 获取GDP数据
    gdp_data = await service.get_gdp(start_date, end_date)
    print(f"获取到 {len(gdp_data)} 条GDP数据")
    for item in gdp_data[:2]:
        print(f"{item['year']}年Q{item['quarter']}: "
              f"GDP {item['gdp']}亿元, 同比增长 {item['gdp_yoy']}%")
    
    # 获取CPI数据
    cpi_data = await service.get_cpi(start_date, end_date)
    print(f"获取到 {len(cpi_data)} 条CPI数据")
    
    # 获取利率数据
    interest_rates = await service.get_interest_rate(start_date, end_date)
    print(f"获取到 {len(interest_rates)} 条利率数据")

asyncio.run(example_get_macro())
```

## 技术指标计算

### 4. 使用 IndicatorService

#### 基础指标计算
```python
import pandas as pd
import numpy as np
from app.services.indicator_service import IndicatorService

def example_calculate_indicators():
    # 创建示例数据（实际应用中应从K线服务获取）
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    df = pd.DataFrame({
        'open': np.random.randn(100).cumsum() + 100,
        'high': np.random.randn(100).cumsum() + 105,
        'low': np.random.randn(100).cumsum() + 95,
        'close': np.random.randn(100).cumsum() + 100,
        'volume': np.random.randint(10000, 1000000, 100)
    }, index=dates)
    
    # 计算移动平均线
    sma_10 = IndicatorService.sma(df, length=10)
    ema_20 = IndicatorService.ema(df, length=20)
    print(f"SMA(10)最新值: {sma_10.iloc[-1]:.2f}")
    print(f"EMA(20)最新值: {ema_20.iloc[-1]:.2f}")
    
    # 计算MACD
    macd_df = IndicatorService.macd(df)
    print(f"MACD: {macd_df.iloc[-1, 0]:.4f}, "
          f"Signal: {macd_df.iloc[-1, 1]:.4f}, "
          f"Histogram: {macd_df.iloc[-1, 2]:.4f}")
    
    # 计算RSI
    rsi = IndicatorService.rsi(df, length=14)
    print(f"RSI(14): {rsi.iloc[-1]:.2f}")
    
    # 计算布林带
    bbands = IndicatorService.bollinger_bands(df)
    print(f"布林带上轨: {bbands.iloc[-1, 0]:.2f}, "
          f"中轨: {bbands.iloc[-1, 1]:.2f}, "
          f"下轨: {bbands.iloc[-1, 2]:.2f}")
    
    # 计算KDJ
    kdj = IndicatorService.kdj(df)
    if kdj is not None:
        print(f"KDJ K值: {kdj.iloc[-1, 0]:.2f}, "
              f"D值: {kdj.iloc[-1, 1]:.2f}, "
              f"J值: {kdj.iloc[-1, 2]:.2f}")
    
    return df

# 运行示例
example_calculate_indicators()
```

#### 批量计算多个指标
```python
def example_batch_indicators():
    # 假设已有K线数据DataFrame
    df = pd.DataFrame(...)  # 包含OHLCV列
    
    indicators = {}
    
    # 趋势指标
    indicators['sma_20'] = IndicatorService.sma(df, length=20)
    indicators['ema_12'] = IndicatorService.ema(df, length=12)
    indicators['macd'] = IndicatorService.macd(df)
    indicators['bbands'] = IndicatorService.bollinger_bands(df)
    
    # 动量指标
    indicators['rsi'] = IndicatorService.rsi(df, length=14)
    indicators['stochastic'] = IndicatorService.stochastic(df)
    indicators['cci'] = IndicatorService.cci(df)
    
    # 成交量指标
    indicators['obv'] = IndicatorService.obv(df)
    indicators['ad'] = IndicatorService.ad(df)
    
    # 波动率指标
    indicators['atr'] = IndicatorService.atr(df, length=14)
    indicators['donchian'] = IndicatorService.donchian(df)
    
    # 综合结果
    result_df = pd.concat(indicators, axis=1)
    print(f"计算了 {len(indicators)} 个指标")
    print(result_df.tail())
    
    return result_df
```

### 5. 自定义指标

#### 创建和使用自定义指标
```python
import asyncio
from app.services.custom_indicator import CustomIndicator, indicator_manager

def example_custom_indicators():
    # 创建自定义指标
    volatility_indicator = CustomIndicator(
        name="daily_volatility",
        expression="(high - low) / close * 100",
        description="日波动率（百分比）"
    )
    
    return_indicator = CustomIndicator(
        name="daily_return",
        expression="(close - open) / open * 100",
        description="日收益率（百分比）"
    )
    
    volume_signal = CustomIndicator(
        name="volume_signal",
        expression="volume > 1000000",
        description="成交量信号（是否超过100万）"
    )
    
    # 注册指标
    indicator_manager.register(volatility_indicator)
    indicator_manager.register(return_indicator)
    indicator_manager.register(volume_signal)
    
    # 使用指标计算
    sample_data = {
        'open': 100.0,
        'high': 105.0,
        'low': 98.0,
        'close': 102.0,
        'volume': 1500000
    }
    
    volatility = volatility_indicator.calculate(sample_data)
    daily_return = return_indicator.calculate(sample_data)
    volume_signal_val = volume_signal.calculate(sample_data)
    
    print(f"日波动率: {volatility:.2f}%")
    print(f"日收益率: {daily_return:.2f}%")
    print(f"成交量信号: {volume_signal_val}")
    
    # 获取所有注册的指标
    all_indicators = indicator_manager.list_indicators()
    print(f"已注册 {len(all_indicators)} 个自定义指标:")
    for name, indicator in all_indicators.items():
        print(f"  - {name}: {indicator.description}")

example_custom_indicators()
```

## 高级用法

### 6. 缓存集成

#### 使用统一缓存接口
```python
import asyncio
from app.core.cache import cache

async def example_cache_usage():
    # 设置缓存
    await cache.set("stock:000001:price", 15.80, ttl=300)  # 5分钟过期
    await cache.set("user:123:preferences", {"theme": "dark", "lang": "zh"})
    
    # 获取缓存
    price = await cache.get("stock:000001:price")
    prefs = await cache.get("user:123:preferences")
    
    print(f"缓存价格: {price}")
    print(f"缓存偏好: {prefs}")
    
    # 检查缓存是否存在
    exists = await cache.exists("stock:000001:price")
    print(f"缓存存在: {exists}")
    
    # 删除缓存
    await cache.delete("user:123:preferences")
    
    # 验证删除
    exists = await cache.exists("user:123:preferences")
    print(f"删除后存在: {exists}")

asyncio.run(example_cache_usage())
```

### 7. 错误处理

#### 异常处理示例
```python
import asyncio
from app.core.exceptions import DataProviderError, DataServiceError
from app.services.kline_service import KlineDataService

async def example_error_handling():
    service = KlineDataService()
    
    try:
        # 正常请求
        data = await service.get_daily_kline("000001.SZ")
        print(f"获取数据成功: {len(data)} 条")
        
    except DataProviderError as e:
        print(f"数据提供者错误: {e.provider} - {e.message}")
        print(f"原始异常: {e.original_error}")
        
    except DataServiceError as e:
        print(f"数据服务错误: {e.service} - {e.message}")
        
    except ConnectionError as e:
        print(f"网络连接错误: {e}")
        # 重试逻辑...
        
    except Exception as e:
        print(f"未知错误: {type(e).__name__}: {e}")
        # 记录日志并上报

asyncio.run(example_error_handling())
```

## 性能优化建议

### 批量数据获取
```python
async def batch_fetch_kline(symbols, start_date, end_date):
    """批量获取多个股票的K线数据"""
    service = KlineDataService()
    tasks = []
    
    for symbol in symbols:
        task = service.get_daily_kline(symbol, start_date, end_date)
        tasks.append(task)
    
    # 并发执行
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 处理结果
    for symbol, result in zip(symbols, results):
        if isinstance(result, Exception):
            print(f"{symbol} 获取失败: {result}")
        else:
            print(f"{symbol} 获取到 {len(result)} 条数据")
    
    return results
```

### 缓存策略优化
```python
async def get_cached_kline(symbol, start_date, end_date):
    """带缓存的K线数据获取"""
    cache_key = f"kline:{symbol}:{start_date.date()}:{end_date.date()}"
    
    # 尝试从缓存获取
    cached = await cache.get(cache_key)
    if cached is not None:
        print(f"缓存命中: {cache_key}")
        return cached
    
    # 缓存未命中，从服务获取
    print(f"缓存未命中，从API获取: {cache_key}")
    service = KlineDataService()
    data = await service.get_daily_kline(symbol, start_date, end_date)
    
    # 写入缓存（过期时间1小时）
    if data:
        await cache.set(cache_key, data, ttl=3600)
    
    return data
```

## 最佳实践

1. **异步编程**: 所有数据获取操作都是异步的，使用 `asyncio` 进行并发处理
2. **错误处理**: 使用专门的异常类，区分数据源错误和服务错误
3. **缓存使用**: 高频数据使用缓存，设置合理的TTL
4. **频率控制**: 注意Tushare API的频率限制，使用内置的频率控制
5. **资源清理**: 长时间运行的程序注意关闭Redis连接

## 常见问题

### Q: 如何获取更多历史数据？
A: 调整 `start_date` 参数，但注意API可能有限制。建议分批次获取。

### Q: 指标计算需要什么数据格式？
A: 需要包含 `open`, `high`, `low`, `close` 列的DataFrame，可选 `volume` 列。

### Q: 如何添加新的数据源？
A: 参考 `TushareProvider` 实现，继承 `DataProvider` 类并在 `DataSourceFactory` 中注册。

### Q: 缓存失效怎么办？
A: 缓存系统会自动降级到文件缓存，确保服务可用性。

---

*本文档最后更新日期：2025-04-13*