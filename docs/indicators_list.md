# 技术指标列表

本文档列出了 YiCe 项目支持的所有技术指标，基于 `pandas-ta-classic` 库实现。共支持 **35+** 个常用技术指标，涵盖趋势、动量、成交量、波动率等多个维度。

## 指标概览

| 类别 | 指标数量 | 代表指标 |
|------|---------|---------|
| 趋势指标 | 12 | SMA, EMA, MACD, 布林带, Ichimoku |
| 动量指标 | 11 | RSI, KDJ, CCI, ROC, Williams %R |
| 成交量指标 | 5 | OBV, AD, ADX, VWAP, MFI |
| 波动率指标 | 3 | ATR, Donchian Channels |
| 其他指标 | 4 | TEMA, KAMA, MAMA, TRIX |

## 详细指标列表

### 1. 趋势指标 (Trend Indicators)

#### 移动平均线类
| 指标名称 | 函数名 | 参数 | 描述 |
|---------|--------|------|------|
| 简单移动平均线 | `sma()` | `length=10, source="close"` | 简单移动平均 |
| 指数移动平均线 | `ema()` | `length=10, source="close"` | 指数移动平均 |
| 加权移动平均线 | `wma()` | `length=10, source="close"` | 加权移动平均 |
| 三重指数移动平均 | `tema()` | `length=10, source="close"` | 三重指数移动平均 |
| 考夫曼自适应移动平均 | `kama()` | `length=10, source="close"` | 自适应移动平均 |
| MESA自适应移动平均 | `mama()` | `source="close"` | 自适应移动平均（MESA） |

#### 趋势跟踪类
| 指标名称 | 函数名 | 参数 | 描述 |
|---------|--------|------|------|
| MACD | `macd()` | `fast=12, slow=26, signal=9, source="close"` | 移动平均收敛发散 |
| 布林带 | `bollinger_bands()` | `length=20, std=2.0, source="close"` | 布林带通道 |
| 一目均衡表 | `ichimoku()` | `tenkan=9, kijun=26, senkou=52, offset=26` | 日本云图指标 |
| 唐奇安通道 | `donchian()` | `lower_length=20, upper_length=20` | 唐奇安通道 |

### 2. 动量指标 (Momentum Indicators)

#### 振荡器类
| 指标名称 | 函数名 | 参数 | 描述 |
|---------|--------|------|------|
| 相对强弱指数 | `rsi()` | `length=14, source="close"` | 相对强弱指数 |
| KDJ指标 | `kdj()` | `length=14, signal=3, smooth=3` | 随机振荡器变体 |
| 随机振荡器 | `stochastic()` | `k=14, d=3, smooth_k=3` | 随机振荡器 |
| 商品通道指数 | `cci()` | `length=20` | 商品通道指数 |
| 变动率指标 | `roc()` | `length=10, source="close"` | 价格变动率 |
| 威廉指标 | `willr()` | `length=14` | 威廉百分比范围 |
| 钱德动量振荡器 | `cmo()` | `length=14, source="close"` | 钱德动量振荡器 |
| 终极振荡器 | `ultosc()` | `fast=7, medium=14, slow=28` | 终极振荡器 |
| 动量振荡器 | `ao()` | `fast=5, slow=34` | 动量振荡器 |
| 确然指标 | `kst()` | `roc1=10, roc2=15, roc3=20, roc4=30, sma1=10, sma2=10, sma3=10, sma4=15, signal=9, source="close"` | 确然指标 |

### 3. 成交量指标 (Volume Indicators)

| 指标名称 | 函数名 | 参数 | 描述 |
|---------|--------|------|------|
| 成交量 | `volume()` | 无 | 原始成交量数据 |
| 能量潮 | `obv()` | 无 | 能量潮指标 |
| 累积/派发线 | `ad()` | 无 | 累积派发线 |
| 平均趋向指数 | `adx()` | `length=14` | 平均趋向指数 |
| 成交量加权平均价 | `vwap()` | 无 | 成交量加权平均价 |
| 资金流量指数 | `mfi()` | `length=14` | 资金流量指数 |

### 4. 波动率指标 (Volatility Indicators)

| 指标名称 | 函数名 | 参数 | 描述 |
|---------|--------|------|------|
| 平均真实波幅 | `atr()` | `length=14` | 平均真实波幅 |
| 唐奇安通道 | `donchian()` | `lower_length=20, upper_length=20` | 唐奇安通道（也属于趋势指标） |

### 5. 其他指标 (Other Indicators)

| 指标名称 | 函数名 | 参数 | 描述 |
|---------|--------|------|------|
| 三重指数移动平均 | `tema()` | `length=10, source="close"` | 三重指数移动平均（也属于趋势指标） |
| 考夫曼自适应移动平均 | `kama()` | `length=10, source="close"` | 考夫曼自适应移动平均（也属于趋势指标） |
| MESA自适应移动平均 | `mama()` | `source="close"` | MESA自适应移动平均（也属于趋势指标） |
| TRIX指标 | `trix()` | `length=15, source="close"` | 三重指数平滑平均线 |
| 百分比价格振荡器 | `ppo()` | `fast=12, slow=26, signal=9, source="close"` | 百分比价格振荡器 |
| 相对活力指数 | `rvi()` | `length=14` | 相对活力指数 |

## 指标使用示例

### 基础使用
```python
from app.services.indicator_service import IndicatorService
import pandas as pd

# 假设 df 是包含 OHLCV 数据的 DataFrame
df = pd.DataFrame({
    'open': [...],
    'high': [...],
    'low': [...],
    'close': [...],
    'volume': [...]
})

# 计算单个指标
sma_20 = IndicatorService.sma(df, length=20)
rsi_14 = IndicatorService.rsi(df, length=14)
macd_result = IndicatorService.macd(df)

# 批量计算多个指标
def calculate_all_indicators(df):
    indicators = {}
    
    # 趋势指标
    indicators['SMA_20'] = IndicatorService.sma(df, 20)
    indicators['EMA_12'] = IndicatorService.ema(df, 12)
    indicators['MACD'] = IndicatorService.macd(df)
    indicators['BBANDS'] = IndicatorService.bollinger_bands(df)
    
    # 动量指标
    indicators['RSI_14'] = IndicatorService.rsi(df, 14)
    indicators['KDJ'] = IndicatorService.kdj(df)
    indicators['CCI_20'] = IndicatorService.cci(df)
    
    # 成交量指标
    indicators['OBV'] = IndicatorService.obv(df)
    indicators['ADX_14'] = IndicatorService.adx(df, 14)
    
    # 波动率指标
    indicators['ATR_14'] = IndicatorService.atr(df, 14)
    
    return indicators
```

### 参数调优示例
```python
# 不同参数的MACD
macd_fast = IndicatorService.macd(df, fast=8, slow=17, signal=9)

# 不同周期的布林带
bbands_tight = IndicatorService.bollinger_bands(df, length=10, std=1.5)
bbands_wide = IndicatorService.bollinger_bands(df, length=50, std=2.5)

# 不同长度的RSI
rsi_short = IndicatorService.rsi(df, length=7)
rsi_long = IndicatorService.rsi(df, length=21)

# 不同参数的KDJ
kdj_fast = IndicatorService.kdj(df, length=9, signal=3, smooth=3)
kdj_slow = IndicatorService.kdj(df, length=21, signal=5, smooth=5)
```

## 指标组合策略示例

### 趋势跟踪策略
```python
def trend_following_signals(df):
    """趋势跟踪信号生成"""
    signals = pd.DataFrame(index=df.index)
    
    # 计算指标
    sma_20 = IndicatorService.sma(df, 20)
    sma_50 = IndicatorService.sma(df, 50)
    macd = IndicatorService.macd(df)
    rsi = IndicatorService.rsi(df, 14)
    
    # 生成信号
    # 1. 移动平均线交叉
    signals['sma_crossover'] = sma_20 > sma_50
    
    # 2. MACD信号
    signals['macd_bullish'] = macd.iloc[:, 0] > macd.iloc[:, 1]  # MACD > Signal
    
    # 3. RSI超买超卖
    signals['rsi_oversold'] = rsi < 30
    signals['rsi_overbought'] = rsi > 70
    
    # 综合信号
    signals['buy_signal'] = (
        signals['sma_crossover'] & 
        signals['macd_bullish'] & 
        signals['rsi_oversold']
    )
    
    signals['sell_signal'] = (
        (~signals['sma_crossover']) & 
        (~signals['macd_bullish']) & 
        signals['rsi_overbought']
    )
    
    return signals
```

### 均值回归策略
```python
def mean_reversion_signals(df):
    """均值回归信号生成"""
    signals = pd.DataFrame(index=df.index)
    
    # 计算布林带
    bbands = IndicatorService.bollinger_bands(df, length=20, std=2)
    
    # 计算RSI
    rsi = IndicatorService.rsi(df, 14)
    
    # 布林带突破信号
    upper_band = bbands.iloc[:, 0]
    lower_band = bbands.iloc[:, 2]
    
    signals['bb_upper_break'] = df['close'] > upper_band
    signals['bb_lower_break'] = df['close'] < lower_band
    
    # RSI极端值信号
    signals['rsi_extreme_low'] = rsi < 20
    signals['rsi_extreme_high'] = rsi > 80
    
    # 均值回归信号
    signals['mean_reversion_buy'] = signals['bb_lower_break'] & signals['rsi_extreme_low']
    signals['mean_reversion_sell'] = signals['bb_upper_break'] & signals['rsi_extreme_high']
    
    return signals
```

## 指标计算注意事项

### 数据要求
1. **必需列**: `open`, `high`, `low`, `close`
2. **可选列**: `volume`（用于成交量指标）
3. **数据质量**: 确保没有NaN值，特别是价格数据

### 计算顺序
某些指标依赖于其他指标的计算结果：
1. 先计算基础指标（SMA, EMA等）
2. 再计算衍生指标（MACD依赖EMA，KDJ依赖Stochastic等）

### 性能考虑
1. **批量计算**: 对于大量数据，建议批量计算所有需要的指标
2. **缓存结果**: 频繁使用的指标结果可以缓存
3. **增量计算**: 实时场景下考虑增量更新指标值

## 自定义指标扩展

除了内置指标，系统支持自定义指标：

```python
from app.services.custom_indicator import CustomIndicator

# 创建自定义指标
custom = CustomIndicator(
    name="my_custom_indicator",
    expression="(close - sma_20) / sma_20 * 100",  # 需要先计算sma_20
    description="价格相对于20日均线的偏离百分比"
)

# 使用自定义指标
data = {
    'close': 100.0,
    'sma_20': 95.0  # 需要先计算并传入
}
result = custom.calculate(data)
```

## 指标验证与测试

### 验证指标计算结果
```python
def validate_indicator_calculation():
    """验证指标计算正确性"""
    # 创建测试数据
    test_data = pd.DataFrame({
        'open': [100, 101, 102, 103, 104],
        'high': [105, 106, 107, 108, 109],
        'low': [98, 99, 100, 101, 102],
        'close': [102, 103, 104, 105, 106],
        'volume': [1000000, 1200000, 1100000, 1300000, 1400000]
    })
    
    # 计算指标
    sma = IndicatorService.sma(test_data, 3)
    rsi = IndicatorService.rsi(test_data, 3)
    
    # 验证结果
    assert len(sma) == len(test_data), "SMA结果长度不匹配"
    assert len(rsi) == len(test_data), "RSI结果长度不匹配"
    assert not sma.isnull().all(), "SMA结果全为NaN"
    
    print("指标计算验证通过")
```

## 故障排除

### 常见问题
1. **指标返回NaN值**: 检查数据是否包含NaN，或周期是否足够长
2. **计算速度慢**: 考虑减少指标数量或使用更短的计算周期
3. **内存占用高**: 对于大数据集，考虑分块计算

### 错误处理
```python
try:
    result = IndicatorService.rsi(df, length=14)
except ValueError as e:
    print(f"数据验证失败: {e}")
except Exception as e:
    print(f"指标计算错误: {e}")
```

## 参考资料

1. [pandas-ta-classic 文档](https://github.com/twopirllc/pandas-ta)
2. [Technical Analysis Indicators Explained](https://www.investopedia.com/terms/t/technicalanalysis.asp)
3. [Stock Indicators for Python](https://daveskender.github.io/Stock.Indicators.Python/)

---

*本文档最后更新日期：2025-04-13*