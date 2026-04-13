# Draft: 奕策（YiCe）Phase 2: 数据源对接 + 技术指标计算

## 阶段概述
基于Phase 1搭建的项目框架，本阶段将实现数据源对接层和技术指标计算套件。

## 研究发现（2026年4月最新）

### 金融数据源库现状
1. **AKShare 1.18.54** (2026-04-08最新)
   - 18.1k Stars，持续维护
   - 免费开源，接口统一
   - 覆盖A股、港股、美股、基金、外汇、宏观经济数据
   - 提供HTTP API版本AKTools
   - 注意：底层是爬虫，需注意WAF封锁和Rate Limiting

2. **Tushare Pro**
   - Data-as-a-Service路线，标准化DataFrame
   - 核心高频数据需要积分
   - 频控严格，需实现RateLimiter

3. **聚宽JQData**
   - 机构级数据源，质量高
   - 需付费订阅

### 技术指标计算库
1. **pandas-ta-classic 0.4.47** (2026-03-17)
   - 212个技术指标（150个指标+62个TA-Lib蜡烛图模式）
   - 社区维护版本，活跃开发
   - 支持uv和pip安装
   - 自动集成TA-Lib（如果已安装）

2. **TA-Lib 0.6.8** (2025-10-20)
   - 150+指标，C语言内核，性能好
   - 支持Python 3.9-3.14
   - 提供二进制wheel，无需编译

3. **numpy-financial**
   - 金融计算函数补充

### MCP搜索工具
1. **Exa MCP Server**
   - `exa-code`：代码上下文搜索
   - `web_search_exa`：实时网页搜索
   - `company_research`：企业信息调研
   - 远程服务：https://mcp.exa.ai/mcp

2. **Tavily MCP**
   - `tavily_search`：AI驱动的实时搜索
   - `tavily_extract`：文档内容提取
   - `tavily_crawl`：网站爬取
   - LangChain官方集成：`langchain-tavily`

## Phase 2 目标

### 核心功能
1. **数据源抽象层实现**
   - DataProvider接口具体实现
   - TushareProvider（优先实现）
   - AKShareProvider（预留接口，暂不实现）
   - JQDataProvider（预留接口）
   - 数据源配置管理

2. **数据获取模块**
   - 历史K线数据获取（日K、周K、月K）- Tushare
   - 成交量数据获取 - Tushare
   - 基本面数据获取（财务报表、公司信息）- Tushare
   - 宏观经济数据获取 - Tushare

3. **数据缓存层**
   - Redis缓存配置
   - 缓存策略设计（TTL、失效策略）
   - 本地文件缓存备选方案

4. **技术指标计算套件**
   - 集成pandas-ta-classic
   - 封装常用指标（MA、KDJ、RSI、BOLL、MACD等）
   - 指标计算接口统一化
   - 自定义指标支持

5. **数据预处理模块**
   - 数据清洗
   - 缺失值处理
   - 除权除息处理
   - 数据对齐

### 技术决策
- **数据源优先**：仅实现Tushare，AKShare等其他数据源暂时搁置
- **技术指标库**：pandas-ta-classic + TA-Lib（可选加速）
- **缓存方案**：Redis（主要）+ 本地文件（备选）
- **A股专注**：初期仅实现A股数据源

### 必须实现
- Tushare数据源完整适配
- 30+常用技术指标
- 数据缓存机制
- 错误处理和重试机制

### 暂不实现
- AKShare数据源适配
- JQData数据源适配
- 社交媒体爬虫（后期付费功能）
- 国际市场数据
- 实时行情推送（后期）

## 任务分解

### Wave 1: 数据源实现
1. TushareProvider实现
2. 数据源工厂类（仅Tushare）
3. 数据源配置系统（Tushare Token管理）

### Wave 2: 数据获取模块
4. K线数据获取服务
5. 基本面数据获取服务
6. 宏观经济数据获取服务
7. 数据统一格式转换

### Wave 3: 缓存层
8. Redis缓存集成
9. 缓存策略实现
10. 本地文件缓存备选

### Wave 4: 技术指标套件
11. pandas-ta-classic集成
12. 常用指标封装（MA、KDJ、RSI、BOLL等）
13. 指标计算服务
14. 自定义指标支持接口

### Wave 5: 测试与优化
15. 数据获取测试
16. 指标计算准确性验证
17. 性能优化
18. 错误处理完善
19. 文档更新

## 关键技术点

### 数据源容错设计
- 重试装饰器（tenacity）
- RateLimiter实现
- Tushare API错误处理与重试

### 技术指标封装策略
```python
# 统一接口示例
class TechnicalIndicatorService:
    def calculate_ma(self, data, period=5, type='sma'):
        pass
    
    def calculate_kdj(self, data, n=9, m1=3, m2=3):
        pass
    
    # ... 更多指标
```

### 缓存键设计
```
格式: yice:data:{provider}:{data_type}:{symbol}:{params}
示例: yice:data:tushare:kline:000001.SZ:daily:20240101-20241231
```

## 依赖关系
- 依赖Phase 1完成的项目架构
- 为Phase 3（Agent开发）提供数据支撑
