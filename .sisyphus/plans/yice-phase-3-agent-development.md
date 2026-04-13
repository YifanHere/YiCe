# 奕策（YiCe）- Phase 3: Agent团队开发

## TL;DR

&gt; **Quick Summary**: 实现4个分析师Agent、宏观分析师、AHP决策引擎、风控交易员，构建完整的LangGraph工作流
&gt; 
&gt; **Deliverables**:
&gt; - 技术面/基本面/消息面/情绪面分析师Agent
&gt; - 宏观经济/市场分析师Agent（权重分配）
&gt; - AHP层次分析法决策引擎
&gt; - 风险控制交易员Agent
&gt; - 完整的LangGraph工作流
&gt; - Markdown格式报告生成
&gt; 
&gt; **Estimated Effort**: Large
&gt; **Parallel Execution**: YES - 5 waves
&gt; **Critical Path**: Agent框架 → 分析师Agent → 决策引擎 → LangGraph → 集成测试

---

## Context

### Original Request
基于Phase 2完成的数据源和技术指标计算，实现核心的Agent工作流。

### Key Decisions (from Draft)
- **LLM集成**: 支持多种提供商（OpenAI、Anthropic、DeepSeek等）
- **结构化输出**: 使用Pydantic模型确保输出格式一致
- **工作流持久化**: LangGraph checkpoint保存执行状态
- **人在回路**: 关键决策点支持人工干预（可选）
- **暂不深入**: Agent工作流复杂优化、社交媒体情绪分析、实盘交易接口

### Research Findings
- **TradingAgents**: 49.8k Stars参考项目，分析师团队→多空辩论→风控→决策
- **AHP层次分析法**: 1-9标度，一致性检验CR&lt;0.1
- **LangGraph 1.1.6**: 持久化执行、人在回路、全面内存管理

---

## Work Objectives

### Core Objective
构建完整的Agent团队和LangGraph工作流，实现从数据输入到最终分析报告的全流程自动化。

### Concrete Deliverables
- [ ] Agent基类设计与LLM集成模块
- [ ] 技术面分析师Agent（K线+指标→报告+1-9标度）
- [ ] 基本面分析师Agent（财务数据→报告+1-9标度）
- [ ] 消息面分析师Agent（Exa/Tavily MCP搜索→报告+1-9标度）
- [ ] 情绪面分析师Agent（简化版）
- [ ] 宏观经济/市场分析师Agent（权重分配）
- [ ] AHP决策引擎实现
- [ ] 风险控制交易员Agent
- [ ] 完整的LangGraph工作流（State+Nodes+Edges）
- [ ] 后端API端点（/analyze/{symbol}）

### Definition of Done
- [ ] `uv run pytest backend/tests/test_agents.py` → PASS
- [ ] 能成功运行完整工作流分析000001.SZ
- [ ] 所有Agent输出符合Pydantic模型格式
- [ ] AHP计算正确
- [ ] 最终生成完整的Markdown报告

### Must Have
- 4个基础分析师Agent（技术面、基本面、消息面、情绪面）
- 宏观分析师Agent（权重分配）
- AHP决策引擎
- 风控交易员Agent
- 完整的LangGraph工作流
- Markdown格式报告生成
- 结构化输出（Pydantic）

### Must NOT Have (Guardrails)
- 不过度优化Agent工作流（用户明确前期可调整）
- 不实现社交媒体情绪分析（后期付费功能）
- 不实现实盘交易接口
- 不添加过度复杂的Prompt工程

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: YES
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
Wave 1 (Start Immediately - 基础Agent框架):
├── Task 1: Agent基类设计
├── Task 2: LLM集成模块
├── Task 3: 结构化输出模型定义
└── Task 4: Prompt模板系统

Wave 2 (After Wave 1 - 分析师Agent开发):
├── Task 5: 技术面分析师Agent
├── Task 6: 基本面分析师Agent
├── Task 7: 消息面分析师Agent（含MCP搜索集成）
└── Task 8: 情绪面分析师Agent（简化版）

Wave 3 (After Wave 2 - 决策与风控):
├── Task 9: 宏观经济/市场分析师Agent
├── Task 10: AHP决策引擎实现
├── Task 11: 风险控制交易员Agent
└── Task 12: 报告生成模块

Wave 4 (After Wave 3 - LangGraph工作流):
├── Task 13: State定义与管理
├── Task 14: Graph节点设计
├── Task 15: 边与条件逻辑
└── Task 16: Checkpoint配置

Wave 5 (After All - 集成测试):
├── Task 17: 端到端工作流测试
├── Task 18: 输出质量验证
├── Task 19: 错误处理完善
└── Task 20: 文档更新
```

### Dependency Matrix

- **1-4**: - - 5-8, 1
- **5-8**: 1-4 - 9-12, 2
- **9-12**: 5-8 - 13-16, 3
- **13-16**: 9-12 - 17-20, 4
- **17-20**: 13-16 - Final, 5

### Agent Dispatch Summary

- **1**: **4** - T1-T4 → `deep`
- **2**: **4** - T5-T8 → `deep`
- **3**: **4** - T9-T12 → `deep`
- **4**: **4** - T13-T16 → `deep`
- **5**: **4** - T17-T20 → `quick`

---

## TODOs

- [ ] 1. Agent基类设计

  **What to do**:
  - 创建BaseAgent抽象基类
  - 定义统一的接口（run方法、输入输出模型）
  - 实现公共功能（日志、错误处理）
  - 设计Prompt模板系统

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 2, 3, 4)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: None

  **Acceptance Criteria**:
  - [ ] BaseAgent类创建完成
  - [ ] 接口定义清晰

  **Commit**: YES
  - Message: `feat: design Agent base class`

---

- [ ] 2. LLM集成模块

  **What to do**:
  - 创建LLMService类
  - 支持多种LLM提供商（OpenAI、Anthropic、DeepSeek等）
  - 实现统一的调用接口
  - 添加重试和错误处理
  - 支持结构化输出

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 1, 3, 4)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: None

  **Acceptance Criteria**:
  - [ ] LLMService创建完成
  - [ ] 能调用至少一种LLM

  **Commit**: YES
  - Message: `feat: implement LLM integration module`

---

- [ ] 3. 结构化输出模型定义

  **What to do**:
  - 定义AnalysisReport Pydantic模型（report、sentiment_score、key_points）
  - 定义WeightAssignment Pydantic模型（四个权重，和为1）
  - 定义FinalReport模型
  - 添加模型验证

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 1, 2, 4)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: None

  **Acceptance Criteria**:
  - [ ] 所有Pydantic模型定义完成
  - [ ] 验证逻辑正确

  **Commit**: YES
  - Message: `feat: define structured output models`

---

- [ ] 4. Prompt模板系统

  **What to do**:
  - 创建PromptTemplate类
  - 为每个分析师Agent设计专业的Prompt
  - 支持Prompt参数化
  - 支持从文件加载Prompt

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 1, 2, 3)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: None

  **Acceptance Criteria**:
  - [ ] Prompt模板系统创建完成
  - [ ] 各分析师Prompt已设计

  **Commit**: YES
  - Message: `feat: add Prompt template system`

---

- [ ] 5. 技术面分析师Agent

  **What to do**:
  - 继承BaseAgent创建TechnicalAnalystAgent
  - 输入：K线数据、成交量、技术指标
  - 输出：AnalysisReport（Markdown报告 + 1-9多空标度）
  - 分析内容：趋势判断、支撑阻力、指标信号

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 6, 7, 8)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Acceptance Criteria**:
  - [ ] TechnicalAnalystAgent创建完成
  - [ ] 能生成分析报告和多空标度

  **Commit**: YES
  - Message: `feat: implement technical analyst Agent`

---

- [ ] 6. 基本面分析师Agent

  **What to do**:
  - 继承BaseAgent创建FundamentalAnalystAgent
  - 输入：财务报表、公司信息、行业数据
  - 输出：AnalysisReport（Markdown报告 + 1-9多空标度）
  - 分析内容：估值、成长性、盈利能力、财务健康

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5, 7, 8)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Acceptance Criteria**:
  - [ ] FundamentalAnalystAgent创建完成
  - [ ] 能生成分析报告和多空标度

  **Commit**: YES
  - Message: `feat: implement fundamental analyst Agent`

---

- [ ] 7. 消息面分析师Agent（含MCP搜索集成）

  **What to do**:
  - 继承BaseAgent创建NewsAnalystAgent
  - 集成Exa或Tavily MCP搜索
  - 输入：最新资讯
  - 输出：AnalysisReport（Markdown报告 + 1-9多空标度）
  - 分析内容：利好/利空消息、事件影响、市场反应

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5, 6, 8)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Acceptance Criteria**:
  - [ ] NewsAnalystAgent创建完成
  - [ ] MCP搜索集成完成
  - [ ] 能生成分析报告和多空标度

  **Commit**: YES
  - Message: `feat: implement news analyst Agent (with MCP)`

---

- [ ] 8. 情绪面分析师Agent（简化版）

  **What to do**:
  - 继承BaseAgent创建SentimentAnalystAgent
  - 初期简化实现：基于消息面情绪分析
  - 预留社交媒体爬虫接口
  - 输出：AnalysisReport（Markdown报告 + 1-9多空标度）

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5, 6, 7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Acceptance Criteria**:
  - [ ] SentimentAnalystAgent创建完成（简化版）
  - [ ] 预留社交媒体接口

  **Commit**: YES
  - Message: `feat: implement sentiment analyst Agent (simplified)`

---

- [ ] 9. 宏观经济/市场分析师Agent

  **What to do**:
  - 继承BaseAgent创建MacroAnalystAgent
  - 输入：宏观经济数据、市场趋势资讯
  - 输出：WeightAssignment（技术面/基本面/消息面/情绪面权重）
  - 分析内容：当前市场环境、主导风格、板块轮动

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 10, 11, 12)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 5, 6, 7, 8

  **Acceptance Criteria**:
  - [ ] MacroAnalystAgent创建完成
  - [ ] 能输出权重分配（和为1）

  **Commit**: YES
  - Message: `feat: implement macroeconomic analyst Agent`

---

- [ ] 10. AHP决策引擎实现

  **What to do**:
  - 创建AHPEngine类
  - 实现1-9标度归一化（到0-1）
  - 实现加权求和计算最终得分
  - 添加结果验证

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 9, 11, 12)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 5, 6, 7, 8

  **Acceptance Criteria**:
  - [ ] AHPEngine创建完成
  - [ ] 计算逻辑正确

  **Commit**: YES
  - Message: `feat: implement AHP decision engine`

---

- [ ] 11. 风险控制交易员Agent

  **What to do**:
  - 继承BaseAgent创建RiskControlTraderAgent
  - 输入：综合得分 + 各分析报告
  - 输出：总结报告 + 具体交易操作建议
  - 内容：风险提示、仓位建议、操作策略

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 9, 10, 12)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 5, 6, 7, 8

  **Acceptance Criteria**:
  - [ ] RiskControlTraderAgent创建完成
  - [ ] 能生成总结和操作建议

  **Commit**: YES
  - Message: `feat: implement risk control trader Agent`

---

- [ ] 12. 报告生成模块

  **What to do**:
  - 创建ReportGenerator类
  - 整合所有Agent的输出
  - 生成最终的Markdown报告
  - 添加报告格式化和美化

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 9, 10, 11)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 5, 6, 7, 8

  **Acceptance Criteria**:
  - [ ] ReportGenerator创建完成
  - [ ] 能生成完整的最终报告

  **Commit**: YES
  - Message: `feat: implement report generation module`

---

- [ ] 13. State定义与管理

  **What to do**:
  - 定义AgentState TypedDict
  - 包含所有必要字段（symbol、kline_data、各report、weights、final_score等）
  - 使用add_messages处理消息历史

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 14, 15, 16)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 17, 18, 19, 20
  - **Blocked By**: Tasks 9, 10, 11, 12

  **Acceptance Criteria**:
  - [ ] AgentState定义完成
  - [ ] 字段完整

  **Commit**: YES
  - Message: `feat: define LangGraph State`

---

- [ ] 14. Graph节点设计

  **What to do**:
  - 创建数据获取节点
  - 创建指标计算节点
  - 创建4个分析师并行节点
  - 创建宏观分析师节点
  - 创建AHP计算节点
  - 创建风控交易员节点
  - 创建报告生成节点

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 13, 15, 16)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 17, 18, 19, 20
  - **Blocked By**: Tasks 9, 10, 11, 12

  **Acceptance Criteria**:
  - [ ] 所有节点创建完成
  - [ ] 节点逻辑正确

  **Commit**: YES
  - Message: `feat: design LangGraph nodes`

---

- [ ] 15. 边与条件逻辑

  **What to do**:
  - 连接节点形成完整工作流
  - 实现并行执行（4个分析师同时运行）
  - 添加条件边（错误处理）
  - 设计流程控制

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 13, 14, 16)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 17, 18, 19, 20
  - **Blocked By**: Tasks 9, 10, 11, 12

  **Acceptance Criteria**:
  - [ ] 边与条件逻辑实现完成
  - [ ] 工作流能正常流转

  **Commit**: YES
  - Message: `feat: implement edges and conditional logic`

---

- [ ] 16. Checkpoint配置

  **What to do**:
  - 配置LangGraph checkpoint
  - 选择持久化存储（SQLite或Redis）
  - 实现工作流状态保存和恢复
  - 支持中断后继续

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 13, 14, 15)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 17, 18, 19, 20
  - **Blocked By**: Tasks 9, 10, 11, 12

  **Acceptance Criteria**:
  - [ ] Checkpoint配置完成
  - [ ] 状态能正常保存和恢复

  **Commit**: YES
  - Message: `feat: configure LangGraph checkpoint`

---

(剩余任务17-20：端到端测试、输出质量验证、错误处理完善、文档更新，请参考Phase 2类似任务格式)

---

---

## Final Verification Wave

- [ ] F1. **Plan Compliance Audit** — `oracle`
- [ ] F2. **Code Quality Review** — `unspecified-high`
- [ ] F3. **Real Manual QA** — `unspecified-high`
- [ ] F4. **Scope Fidelity Check** — `deep`

---

## Commit Strategy

- **1**: `feat: design Agent base class`
- **2**: `feat: implement LLM integration module`
- **3**: `feat: define structured output models`
- **4**: `feat: add Prompt template system`
- **5**: `feat: implement technical analyst Agent`
- **6**: `feat: implement fundamental analyst Agent`
- **7**: `feat: implement news analyst Agent (with MCP)`
- **8**: `feat: implement sentiment analyst Agent (simplified)`
- **9**: `feat: implement macroeconomic analyst Agent`
- **10**: `feat: implement AHP decision engine`
- **11**: `feat: implement risk control trader Agent`
- **12**: `feat: implement report generation module`
- **13**: `feat: define LangGraph State`
- **14**: `feat: design LangGraph nodes`
- **15**: `feat: implement edges and conditional logic`
- **16**: `feat: configure LangGraph checkpoint`
- **17**: `test: end-to-end workflow tests`
- **18**: `test: output quality verification`
- **19**: `fix: error handling improvement`
- **20**: `docs: update documentation`

---

## Success Criteria

### Verification Commands
```bash
cd backend &amp;&amp; uv run pytest tests/test_agents.py  # Expected: all tests pass
cd backend &amp;&amp; uv run python -c "from app.workflows.analysis_graph import AnalysisGraph; g = AnalysisGraph(); print('OK')"  # Expected: OK
```

### Final Checklist
- [ ] 所有Agent实现完成
- [ ] AHP引擎计算正确
- [ ] LangGraph工作流完整
- [ ] 所有测试通过
- [ ] 能生成完整的分析报告
