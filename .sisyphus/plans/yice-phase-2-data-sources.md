# 奕策（YiCe）- Phase 2: 数据源对接 + 技术指标计算

## TL;DR

&gt; **Quick Summary**: 实现Tushare数据源对接、数据缓存层、技术指标计算套件，为后续Agent开发提供数据支撑
&gt; 
&gt; **Deliverables**:
&gt; - TushareProvider完整实现
&gt; - 数据获取服务（K线、基本面、宏观经济）
&gt; - Redis缓存层
&gt; - pandas-ta-classic技术指标套件（30+常用指标）
&gt; - 数据预处理模块
&gt; 
&gt; **Estimated Effort**: Medium
&gt; **Parallel Execution**: YES - 5 waves
&gt; **Critical Path**: TushareProvider → 数据获取 → 缓存层 → 指标套件 → 测试

---

## Context

### Original Request
基于Phase 1搭建的项目框架，实现数据源对接层和技术指标计算套件。

### Key Decisions (from Draft)
- **数据源优先**：仅实现Tushare，AKShare等其他数据源暂时搁置
- **技术指标库**：pandas-ta-classic 0.4.47 + TA-Lib（可选）
- **缓存方案**：Redis（主要）+ 本地文件（备选）
- **A股专注**：初期仅实现A股数据源

### Research Findings (2026年4月最新)
- **Tushare Pro**: Data-as-a-Service，标准化DataFrame，需Token
- **pandas-ta-classic 0.4.47**: 212个技术指标，社区活跃维护
- **TA-Lib 0.6.8**: 150+指标，C语言内核，性能好
- **Redis**: 高效缓存，支持TTL和失效策略

---

## Work Objectives

### Core Objective
建立完整的数据层，包括Tushare数据源对接、数据缓存、技术指标计算，为Agent开发提供可靠的数据支撑。

### Concrete Deliverables
- [ ] TushareProvider实现（K线、基本面、宏观经济数据）
- [ ] 数据源工厂类与配置系统
- [ ] Redis缓存集成与策略实现
- [ ] pandas-ta-classic集成与30+常用指标封装
- [ ] 数据预处理模块（清洗、缺失值、除权除息）
- [ ] 数据获取API端点

### Definition of Done
- [ ] `uv run pytest backend/tests/test_data.py` → PASS
- [ ] 能成功获取000001.SZ的日K数据
- [ ] 能成功计算MA、KDJ、RSI等常用指标
- [ ] Redis缓存正常工作（TTL生效）
- [ ] 数据预处理模块能处理常见异常情况

### Must Have
- Tushare数据源完整适配（日K/周K/月K、基本面、宏观经济）
- 30+常用技术指标（MA、KDJ、RSI、BOLL、MACD等）
- 数据缓存机制（Redis）
- 错误处理和重试机制（tenacity + RateLimiter）
- 类型安全（Pydantic模型）

### Must NOT Have (Guardrails)
- 不实现AKShare数据源（预留接口）
- 不实现JQData数据源（预留接口）
- 不实现社交媒体爬虫（后期付费功能）
- 不实现国际市场数据
- 不实现实时行情推送（后期）
- 不过早优化性能

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: YES (from Phase 1)
- **Automated tests**: YES (Tests-after)
- **Framework**: pytest (后端)
- **Agent-Executed QA**: MANDATORY for all tasks

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately - 数据源实现):
├── Task 1: TushareProvider实现
├── Task 2: 数据源工厂类（仅Tushare）
└── Task 3: 数据源配置系统（Tushare Token管理）

Wave 2 (After Wave 1 - 数据获取模块):
├── Task 4: K线数据获取服务
├── Task 5: 基本面数据获取服务
├── Task 6: 宏观经济数据获取服务
└── Task 7: 数据统一格式转换

Wave 3 (After Wave 2 - 缓存层):
├── Task 8: Redis缓存集成
├── Task 9: 缓存策略实现
└── Task 10: 本地文件缓存备选

Wave 4 (After Wave 3 - 技术指标套件):
├── Task 11: pandas-ta-classic集成
├── Task 12: 常用指标封装（MA、KDJ、RSI、BOLL等）
├── Task 13: 指标计算服务
└── Task 14: 自定义指标支持接口

Wave 5 (After All - 测试与优化):
├── Task 15: 数据获取测试
├── Task 16: 指标计算准确性验证
├── Task 17: 性能优化
├── Task 18: 错误处理完善
└── Task 19: 文档更新
```

### Dependency Matrix

- **1-3**: - - 4-7, 1
- **4-7**: 1-3 - 8-10, 2
- **8-10**: 4-7 - 11-14, 3
- **11-14**: 8-10 - 15-19, 4
- **15-19**: 11-14 - Final, 5

### Agent Dispatch Summary

- **1**: **3** - T1-T3 → `quick`
- **2**: **4** - T4-T7 → `quick`
- **3**: **3** - T8-T10 → `quick`
- **4**: **4** - T11-T14 → `deep`
- **5**: **5** - T15-T19 → `quick`

---

## TODOs

- [ ] 1. TushareProvider实现

  **What to do**:
  - 实现DataProvider接口的Tushare版本
  - 封装Tushare Pro API调用
  - 实现Token管理（从环境变量读取）
  - 基础错误处理
  - 参考Tushare官方文档：https://tushare.pro/document/2

  **Must NOT do**:
  - 不硬编码Token
  - 不过度封装，保持API简洁

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - `visual-engineering`: 无UI需求

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 2, 3)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
  - **Blocked By**: None

  **References**:
  - Tushare官方文档: https://tushare.pro/document/2
  - Phase 1 DataProvider接口设计: `backend/app/core/providers/base.py`

  **Acceptance Criteria**:
  - [ ] TushareProvider类实现DataProvider接口
  - [ ] 能通过环境变量TUSHARE_TOKEN读取Token
  - [ ] 基础API调用能正常工作

  **QA Scenarios**:
  ```
  Scenario: 验证TushareProvider初始化
    Tool: Bash (Python REPL)
    Preconditions: 任务完成，环境变量TUSHARE_TOKEN已设置
    Steps:
      1. 运行 `cd backend &amp;&amp; uv run python`
      2. 执行: `from app.core.providers.tushare_provider import TushareProvider`
      3. 执行: `provider = TushareProvider()`
      4. 验证provider实例创建成功
    Expected Result: provider实例创建成功，无异常
    Evidence: .sisyphus/evidence/task-1-tushare-init.txt

  Scenario: 验证股票列表获取
    Tool: Bash (Python REPL)
    Preconditions: 任务完成
    Steps:
      1. 运行 `cd backend &amp;&amp; uv run python`
      2. 执行provider.get_stock_list()
      3. 验证返回DataFrame包含股票代码和名称
    Expected Result: 返回有效的股票列表DataFrame
    Evidence: .sisyphus/evidence/task-1-stock-list.txt
  ```

  **Commit**: YES
  - Message: `feat: implement TushareProvider`
  - Files: `backend/app/core/providers/tushare_provider.py`

---

- [ ] 2. 数据源工厂类（仅Tushare）

  **What to do**:
  - 创建DataSourceFactory类
  - 实现get_provider()方法，返回TushareProvider实例
  - 预留AKShareProvider、JQDataProvider接口位置

  **Must NOT do**:
  - 不实现AKShareProvider具体逻辑
  - 不实现JQDataProvider具体逻辑

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 1, 3)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 4, 5, 6, 7
  - **Blocked By**: None

  **References**:
  - 工厂模式最佳实践

  **Acceptance Criteria**:
  - [ ] DataSourceFactory类创建完成
  - [ ] get_provider()返回TushareProvider实例

  **QA Scenarios**:
  ```
  Scenario: 验证工厂类返回TushareProvider
    Tool: Bash (Python REPL)
    Preconditions: 任务完成
    Steps:
      1. 运行 `cd backend &amp;&amp; uv run python`
      2. 执行: `from app.core.providers.factory import DataSourceFactory`
      3. 执行: `provider = DataSourceFactory.get_provider('tushare')`
      4. 验证provider是TushareProvider实例
    Expected Result: provider是TushareProvider类型
    Evidence: .sisyphus/evidence/task-2-factory.txt
  ```

  **Commit**: YES
  - Message: `feat: add DataSourceFactory`
  - Files: `backend/app/core/providers/factory.py`

---

- [ ] 3. 数据源配置系统（Tushare Token管理）

  **What to do**:
  - 在config.py中添加Tushare配置项
  - 支持从环境变量读取TUSHARE_TOKEN
  - 添加配置验证

  **Must NOT do**:
  - 不添加AKShare/JQData的完整配置（仅预留）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 1, 2)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 4, 5, 6, 7
  - **Blocked By**: None

  **References**:
  - Phase 1 config.py: `backend/app/core/config.py`

  **Acceptance Criteria**:
  - [ ] 配置项添加完成
  - [ ] 能从环境变量读取Token

  **QA Scenarios**:
  ```
  Scenario: 验证配置读取
    Tool: Bash (Python REPL)
    Preconditions: 任务完成，环境变量TUSHARE_TOKEN已设置
    Steps:
      1. 运行 `cd backend &amp;&amp; uv run python`
      2. 执行: `from app.core.config import settings`
      3. 验证settings.tushare_token存在且正确
    Expected Result: Token配置读取正确
    Evidence: .sisyphus/evidence/task-3-config.txt
  ```

  **Commit**: YES
  - Message: `feat: add Tushare config`
  - Files: `backend/app/core/config.py`

---

- [ ] 4. K线数据获取服务

  **What to do**:
  - 创建KlineDataService类
  - 封装日K、周K、月K数据获取
  - 实现数据格式标准化（统一列名、日期格式）
  - 添加tenacity重试装饰器
  - 实现RateLimiter（基于Tushare频控要求）

  **Must NOT do**:
  - 不实现实时行情推送（后期）
  - 不实现分钟级数据（初期仅日K及以上）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
  - **Blocked By**: Tasks 1, 2, 3

  **References**:
  - Tushare行情接口: https://tushare.pro/document/2?doc_id=27
  - tenacity文档: https://tenacity.readthedocs.io/

  **Acceptance Criteria**:
  - [ ] 能成功获取000001.SZ的日K数据
  - [ ] 能成功获取周K、月K数据
  - [ ] 数据格式标准化完成

  **QA Scenarios**:
  ```
  Scenario: 验证日K数据获取
    Tool: Bash (Python REPL)
    Preconditions: 任务完成
    Steps:
      1. 运行 `cd backend &amp;&amp; uv run python`
      2. 执行: `from app.services.kline_service import KlineDataService`
      3. 执行: `service = KlineDataService()`
      4. 执行: `df = service.get_daily_kline('000001.SZ', '20240101', '20241231')`
      5. 验证df不为空且包含必要列
    Expected Result: 返回有效的日K数据DataFrame
    Evidence: .sisyphus/evidence/task-4-daily-kline.txt
  ```

  **Commit**: YES
  - Message: `feat: implement kline data service`
  - Files: `backend/app/services/kline_service.py`

---

- [ ] 5. 基本面数据获取服务

  **What to do**:
  - 创建FundamentalDataService类
  - 封装财务报表获取（资产负债表、利润表、现金流量表）
  - 封装公司基本信息获取
  - 封装行业分类数据获取
  - 添加错误处理和重试

  **Must NOT do**:
  - 不实现高频财务数据更新

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 4, 6, 7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
  - **Blocked By**: Tasks 1, 2, 3

  **References**:
  - Tushare财务数据: https://tushare.pro/document/2?doc_id=32

  **Acceptance Criteria**:
  - [ ] 能成功获取000001.SZ的财务报表
  - [ ] 能成功获取公司基本信息

  **QA Scenarios**:
  ```
  Scenario: 验证财务数据获取
    Tool: Bash (Python REPL)
    Preconditions: 任务完成
    Steps:
      1. 运行 `cd backend &amp;&amp; uv run python`
      2. 执行: `from app.services.fundamental_service import FundamentalDataService`
      3. 执行: `service = FundamentalDataService()`
      4. 执行: `df = service.get_financial_report('000001.SZ', 2024, 1)`
      5. 验证df不为空
    Expected Result: 返回有效的财务报表数据
    Evidence: .sisyphus/evidence/task-5-financial.txt
  ```

  **Commit**: YES
  - Message: `feat: implement fundamental data service`
  - Files: `backend/app/services/fundamental_service.py`

---

- [ ] 6. 宏观经济数据获取服务

  **What to do**:
  - 创建MacroDataService类
  - 封装GDP、CPI、PPI等宏观数据获取
  - 封装市场利率数据获取
  - 封装货币供应量数据获取

  **Must NOT do**:
  - 不实现高频宏观数据更新

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 4, 5, 7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
  - **Blocked By**: Tasks 1, 2, 3

  **References**:
  - Tushare宏观数据: https://tushare.pro/document/2?doc_id=131

  **Acceptance Criteria**:
  - [ ] 能成功获取GDP数据
  - [ ] 能成功获取CPI数据

  **QA Scenarios**:
  ```
  Scenario: 验证宏观数据获取
    Tool: Bash (Python REPL)
    Preconditions: 任务完成
    Steps:
      1. 运行 `cd backend &amp;&amp; uv run python`
      2. 执行: `from app.services.macro_service import MacroDataService`
      3. 执行: `service = MacroDataService()`
      4. 执行: `df = service.get_gdp()`
      5. 验证df不为空
    Expected Result: 返回有效的宏观数据
    Evidence: .sisyphus/evidence/task-6-macro.txt
  ```

  **Commit**: YES
  - Message: `feat: implement macroeconomic data service`
  - Files: `backend/app/services/macro_service.py`

---

- [ ] 7. 数据统一格式转换

  **What to do**:
  - 创建DataConverter类
  - 实现Tushare数据格式到内部统一格式的转换
  - 定义Pydantic模型（KlineData、FinancialData等）
  - 实现DataFrame与Pydantic模型的互转

  **Must NOT do**:
  - 不过度设计转换逻辑，保持简洁

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 4, 5, 6)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
  - **Blocked By**: Tasks 1, 2, 3

  **References**:
  - Pydantic文档: https://docs.pydantic.dev/

  **Acceptance Criteria**:
  - [ ] 数据转换模型定义完成
  - [ ] 能成功转换Tushare数据

  **QA Scenarios**:
  ```
  Scenario: 验证数据格式转换
    Tool: Bash (Python REPL)
    Preconditions: 任务完成
    Steps:
      1. 运行 `cd backend &amp;&amp; uv run python`
      2. 执行: `from app.utils.data_converter import DataConverter`
      3. 执行转换验证
    Expected Result: 转换成功
    Evidence: .sisyphus/evidence/task-7-converter.txt
  ```

  **Commit**: YES
  - Message: `feat: implement data format conversion`
  - Files: `backend/app/utils/data_converter.py`, `backend/app/models/data_models.py`

---

- [ ] 8. Redis缓存集成

  **What to do**:
  - 安装redis-py依赖
  - 创建RedisClient类
  - 实现连接池管理
  - 实现基本的get/set/delete操作
  - 实现TTL支持

  **Must NOT do**:
  - 不实现集群模式（初期单机即可）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 9, 10)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 11, 12, 13, 14, 15, 16, 17, 18, 19
  - **Blocked By**: Tasks 4, 5, 6, 7

  **References**:
  - redis-py文档: https://redis-py.readthedocs.io/

  **Acceptance Criteria**:
  - [ ] Redis连接成功
  - [ ] 能成功set/get数据

  **QA Scenarios**:
  ```
  Scenario: 验证Redis连接
    Tool: Bash (Python REPL)
    Preconditions: Redis服务已启动
    Steps:
      1. 运行 `cd backend &amp;&amp; uv run python`
      2. 执行: `from app.core.redis_client import RedisClient`
      3. 执行: `client = RedisClient()`
      4. 执行: `client.set('test_key', 'test_value', ttl=60)`
      5. 执行: `value = client.get('test_key')`
      6. 验证value == 'test_value'
    Expected Result: Redis操作成功
    Evidence: .sisyphus/evidence/task-8-redis.txt
  ```

  **Commit**: YES
  - Message: `feat: integrate Redis cache`
  - Files: `backend/app/core/redis_client.py`, `backend/pyproject.toml`

---

- [ ] 9. 缓存策略实现

  **What to do**:
  - 创建CacheStrategy类
  - 实现缓存键生成（格式：yice:data:{provider}:{data_type}:{symbol}:{params}）
  - 实现不同数据类型的TTL策略（K线: 1小时，基本面: 24小时，宏观: 7天）
  - 实现在数据服务中集成缓存（先查缓存，未命中再查数据源）

  **Must NOT do**:
  - 不实现复杂的缓存失效策略（初期简单TTL即可）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 8, 10)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 11, 12, 13, 14, 15, 16, 17, 18, 19
  - **Blocked By**: Tasks 4, 5, 6, 7

  **References**:
  - Phase 2缓存键设计

  **Acceptance Criteria**:
  - [ ] 缓存键生成正确
  - [ ] TTL策略实现完成
  - [ ] 数据服务缓存集成完成

  **QA Scenarios**:
  ```
  Scenario: 验证缓存策略
    Tool: Bash (Python REPL)
    Preconditions: 任务完成
    Steps:
      1. 验证缓存键生成
      2. 验证数据先查缓存再查数据源
    Expected Result: 缓存策略生效
    Evidence: .sisyphus/evidence/task-9-cache-strategy.txt
  ```

  **Commit**: YES
  - Message: `feat: implement cache strategies`
  - Files: `backend/app/core/cache_strategy.py`

---

- [ ] 10. 本地文件缓存备选

  **What to do**:
  - 创建FileCache类
  - 实现基于pickle或parquet的文件缓存
  - 实现目录管理和清理策略
  - 作为Redis的备选方案（Redis不可用时自动降级）

  **Must NOT do**:
  - 不实现复杂的文件缓存过期管理

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 8, 9)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 11, 12, 13, 14, 15, 16, 17, 18, 19
  - **Blocked By**: Tasks 4, 5, 6, 7

  **References**:
  - parquet文档: https://parquet.apache.org/

  **Acceptance Criteria**:
  - [ ] 文件缓存能正常读写
  - [ ] 降级策略实现完成

  **QA Scenarios**:
  ```
  Scenario: 验证文件缓存
    Tool: Bash (Python REPL)
    Preconditions: 任务完成
    Steps:
      1. 验证文件缓存读写
      2. 验证Redis不可用时降级到文件缓存
    Expected Result: 文件缓存工作正常
    Evidence: .sisyphus/evidence/task-10-file-cache.txt
  ```

  **Commit**: YES
  - Message: `feat: add local file cache fallback`
  - Files: `backend/app/core/file_cache.py`

---

- [ ] 11. pandas-ta-classic集成

  **What to do**:
  - 在pyproject.toml中添加pandas-ta-classic依赖
  - 安装验证
  - （可选）添加TA-Lib依赖作为加速选项
  - 创建基础测试验证导入正常

  **Must NOT do**:
  - 不强制要求TA-Lib（可选）

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 12, 13, 14)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 15, 16, 17, 18, 19
  - **Blocked By**: Tasks 8, 9, 10

  **References**:
  - pandas-ta-classic文档: https://xgboosted.github.io/pandas-ta-classic/

  **Acceptance Criteria**:
  - [ ] pandas-ta-classic安装成功
  - [ ] 能成功导入并使用

  **QA Scenarios**:
  ```
  Scenario: 验证pandas-ta-classic安装
    Tool: Bash (Python REPL)
    Preconditions: 任务完成
    Steps:
      1. 运行 `cd backend &amp;&amp; uv run python`
      2. 执行: `import pandas_ta_classic as ta`
      3. 执行: `print(ta.__version__)`
      4. 验证版本号正确
    Expected Result: 导入成功
    Evidence: .sisyphus/evidence/task-11-pandas-ta.txt
  ```

  **Commit**: YES
  - Message: `feat: integrate pandas-ta-classic`
  - Files: `backend/pyproject.toml`

---

- [ ] 12. 常用指标封装（MA、KDJ、RSI、BOLL等）

  **What to do**:
  - 封装MA（移动平均线：SMA、EMA、WMA）
  - 封装KDJ（随机指标）
  - 封装RSI（相对强弱指标）
  - 封装BOLL（布林带）
  - 封装MACD（指数平滑异同移动平均线）
  - 封装成交量指标（VOL、OBV）
  - 总共封装30+常用指标
  - 每个指标返回统一格式的DataFrame

  **Must NOT do**:
  - 不封装所有212个指标（仅常用30+）

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 11, 13, 14)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 15, 16, 17, 18, 19
  - **Blocked By**: Tasks 8, 9, 10

  **References**:
  - pandas-ta-classic指标列表: https://xgboosted.github.io/pandas-ta-classic/indicators.html

  **Acceptance Criteria**:
  - [ ] 30+常用指标封装完成
  - [ ] 每个指标都能正常计算

  **QA Scenarios**:
  ```
  Scenario: 验证常用指标计算
    Tool: Bash (Python REPL)
    Preconditions: 任务完成，有K线数据
    Steps:
      1. 测试MA计算
      2. 测试KDJ计算
      3. 测试RSI计算
      4. 测试BOLL计算
      5. 测试MACD计算
    Expected Result: 所有指标计算成功
    Evidence: .sisyphus/evidence/task-12-indicators.txt
  ```

  **Commit**: YES
  - Message: `feat: wrap common indicators`
  - Files: `backend/app/services/indicator_service.py`

---

- [ ] 13. 指标计算服务

  **What to do**:
  - 创建IndicatorService类
  - 提供统一的指标计算接口
  - 实现批量指标计算（一次计算多个指标）
  - 实现指标结果缓存
  - 添加数据预处理（清洗、缺失值处理）

  **Must NOT do**:
  - 不实现过度复杂的指标组合

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 11, 12, 14)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 15, 16, 17, 18, 19
  - **Blocked By**: Tasks 8, 9, 10

  **References**:
  - Task 12的指标封装

  **Acceptance Criteria**:
  - [ ] IndicatorService类创建完成
  - [ ] 能批量计算多个指标

  **QA Scenarios**:
  ```
  Scenario: 验证指标计算服务
    Tool: Bash (Python REPL)
    Preconditions: 任务完成
    Steps:
      1. 执行: `from app.services.indicator_service import IndicatorService`
      2. 执行: `service = IndicatorService()`
      3. 执行批量指标计算
    Expected Result: 批量计算成功
    Evidence: .sisyphus/evidence/task-13-indicator-service.txt
  ```

  **Commit**: YES
  - Message: `feat: implement indicator calculation service`
  - Files: `backend/app/services/indicator_service.py`

---

- [ ] 14. 自定义指标支持接口

  **What to do**:
  - 设计自定义指标接口
  - 实现基于Python表达式的自定义指标
  - 实现自定义指标的注册和管理
  - 添加安全沙箱（防止恶意代码）

  **Must NOT do**:
  - 不过度设计自定义指标（初期简单表达式即可）

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 11, 12, 13)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 15, 16, 17, 18, 19
  - **Blocked By**: Tasks 8, 9, 10

  **References**:
  - Python ast模块文档

  **Acceptance Criteria**:
  - [ ] 自定义指标接口设计完成
  - [ ] 能注册和使用简单自定义指标

  **QA Scenarios**:
  ```
  Scenario: 验证自定义指标
    Tool: Bash (Python REPL)
    Preconditions: 任务完成
    Steps:
      1. 注册一个简单自定义指标
      2. 验证能正常计算
    Expected Result: 自定义指标工作正常
    Evidence: .sisyphus/evidence/task-14-custom-indicator.txt
  ```

  **Commit**: YES
  - Message: `feat: add custom indicator support`
  - Files: `backend/app/services/custom_indicator.py`

---

- [ ] 15. 数据获取测试

  **What to do**:
  - 创建tests/test_data.py
  - 编写TushareProvider单元测试
  - 编写KlineDataService测试
  - 编写FundamentalDataService测试
  - 编写MacroDataService测试
  - 使用pytest-mock模拟Tushare API调用

  **Must NOT do**:
  - 不编写需要真实Token的集成测试（单元测试用mock）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 16, 17, 18, 19)
  - **Parallel Group**: Wave 5
  - **Blocks**: None
  - **Blocked By**: Tasks 11, 12, 13, 14

  **References**:
  - pytest文档: https://docs.pytest.org/
  - pytest-mock文档: https://pytest-mock.readthedocs.io/

  **Acceptance Criteria**:
  - [ ] 测试文件创建完成
  - [ ] `uv run pytest tests/test_data.py` → PASS

  **QA Scenarios**:
  ```
  Scenario: 运行数据获取测试
    Tool: Bash
    Preconditions: 任务完成
    Steps:
      1. 运行 `cd backend &amp;&amp; uv run pytest tests/test_data.py -v`
    Expected Result: 所有测试通过
    Evidence: .sisyphus/evidence/task-15-data-tests.txt
  ```

  **Commit**: YES
  - Message: `test: add data fetching tests`
  - Files: `backend/tests/test_data.py`

---

- [ ] 16. 指标计算准确性验证

  **What to do**:
  - 创建tests/test_indicators.py
  - 编写指标计算测试
  - 使用已知正确的数据验证指标计算结果
  - 对比pandas-ta-classic原始结果验证封装正确性
  - 测试自定义指标

  **Must NOT do**:
  - 不跳过准确性验证

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 15, 17, 18, 19)
  - **Parallel Group**: Wave 5
  - **Blocks**: None
  - **Blocked By**: Tasks 11, 12, 13, 14

  **References**:
  - Task 12的指标封装

  **Acceptance Criteria**:
  - [ ] 指标测试文件创建完成
  - [ ] `uv run pytest tests/test_indicators.py` → PASS

  **QA Scenarios**:
  ```
  Scenario: 运行指标计算测试
    Tool: Bash
    Preconditions: 任务完成
    Steps:
      1. 运行 `cd backend &amp;&amp; uv run pytest tests/test_indicators.py -v`
    Expected Result: 所有测试通过
    Evidence: .sisyphus/evidence/task-16-indicator-tests.txt
  ```

  **Commit**: YES
  - Message: `test: add indicator accuracy verification`
  - Files: `backend/tests/test_indicators.py`

---

- [ ] 17. 性能优化

  **What to do**:
  - 添加数据获取性能监控
  - 优化缓存命中率
  - 优化pandas操作（避免copy）
  - 优化指标计算（使用向量化操作）
  - 添加必要的代码注释

  **Must NOT do**:
  - 不过度优化（满足基本性能即可）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 15, 16, 18, 19)
  - **Parallel Group**: Wave 5
  - **Blocks**: None
  - **Blocked By**: Tasks 11, 12, 13, 14

  **References**:
  - pandas性能优化指南

  **Acceptance Criteria**:
  - [ ] 代码通过ruff/flake8检查
  - [ ] 基本性能满足要求

  **QA Scenarios**:
  ```
  Scenario: 验证代码质量
    Tool: Bash
    Preconditions: 任务完成
    Steps:
      1. 运行 `cd backend &amp;&amp; uv run ruff check app/`
    Expected Result: 无错误
    Evidence: .sisyphus/evidence/task-17-code-quality.txt
  ```

  **Commit**: YES
  - Message: `perf: performance optimization`
  - Files: 多个文件

---

- [ ] 18. 错误处理完善

  **What to do**:
  - 完善所有服务的异常处理
  - 定义自定义异常类（DataProviderError、CacheError等）
  - 添加错误日志记录
  - 完善RateLimiter的错误提示
  - 添加友好的错误消息

  **Must NOT do**:
  - 不忽略异常（至少记录日志）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 15, 16, 17, 19)
  - **Parallel Group**: Wave 5
  - **Blocks**: None
  - **Blocked By**: Tasks 11, 12, 13, 14

  **References**:
  - Python异常处理最佳实践

  **Acceptance Criteria**:
  - [ ] 自定义异常类定义完成
  - [ ] 错误处理完善

  **QA Scenarios**:
  ```
  Scenario: 验证错误处理
    Tool: Bash (Python REPL)
    Preconditions: 任务完成
    Steps:
      1. 测试各种错误场景
      2. 验证错误被正确捕获和记录
    Expected Result: 错误处理正确
    Evidence: .sisyphus/evidence/task-18-error-handling.txt
  ```

  **Commit**: YES
  - Message: `fix: error handling improvement`
  - Files: `backend/app/core/exceptions.py`等

---

- [ ] 19. 文档更新

  **What to do**:
  - 更新README.md，添加Phase 2功能说明
  - 添加数据层架构文档
  - 添加API使用示例
  - 添加指标列表文档
  - 更新快速开始指南

  **Must NOT do**:
  - 不写过度冗长的文档

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 15, 16, 17, 18)
  - **Parallel Group**: Wave 5
  - **Blocks**: None
  - **Blocked By**: Tasks 11, 12, 13, 14

  **References**:
  - Phase 1 README.md

  **Acceptance Criteria**:
  - [ ] 文档更新完成
  - [ ] README.md包含Phase 2功能说明

  **QA Scenarios**:
  ```
  Scenario: 验证文档更新
    Tool: Bash (ls + cat)
    Preconditions: 任务完成
    Steps:
      1. 检查文档文件存在
      2. 验证内容完整
    Expected Result: 文档完整
    Evidence: .sisyphus/evidence/task-19-docs.txt
  ```

  **Commit**: YES
  - Message: `docs: update documentation`
  - Files: `README.md`, `docs/`等

---

## Final Verification Wave

- [ ] F1. **Plan Compliance Audit** — `oracle`
- [ ] F2. **Code Quality Review** — `unspecified-high`
- [ ] F3. **Real Manual QA** — `unspecified-high`
- [ ] F4. **Scope Fidelity Check** — `deep`

---

## Commit Strategy

- **1**: `feat: implement TushareProvider`
- **2**: `feat: add DataSourceFactory`
- **3**: `feat: add Tushare config`
- **4**: `feat: implement kline data service`
- **5**: `feat: implement fundamental data service`
- **6**: `feat: implement macroeconomic data service`
- **7**: `feat: data format conversion`
- **8**: `feat: integrate Redis cache`
- **9**: `feat: implement cache strategies`
- **10**: `feat: add local file cache fallback`
- **11**: `feat: integrate pandas-ta-classic`
- **12**: `feat: wrap common indicators`
- **13**: `feat: implement indicator calculation service`
- **14**: `feat: add custom indicator support`
- **15**: `test: data fetching tests`
- **16**: `test: indicator accuracy verification`
- **17**: `perf: performance optimization`
- **18**: `fix: error handling improvement`
- **19**: `docs: update documentation`

---

## Success Criteria

### Verification Commands
```bash
cd backend &amp;&amp; uv run pytest tests/test_data.py  # Expected: all tests pass
cd backend &amp;&amp; uv run python -c "from app.core.providers.factory import DataSourceFactory; p = DataSourceFactory.get_provider('tushare'); print('OK')"  # Expected: OK
```

### Final Checklist
- [ ] TushareProvider完整实现
- [ ] 30+技术指标可用
- [ ] Redis缓存正常工作
- [ ] 所有测试通过
- [ ] 文档更新完成
