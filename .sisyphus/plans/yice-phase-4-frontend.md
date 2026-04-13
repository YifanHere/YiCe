# 奕策（YiCe）- Phase 4: 前端界面开发

## TL;DR

&gt; **Quick Summary**: 实现Vue 3前端界面，包括仿TradingView K线看板、Agent工作流可视化、分析报告展示
&gt; 
&gt; **Deliverables**:
&gt; - 首页/股票搜索页
&gt; - 股票详情页（仿TradingView K线看板）
&gt; - 分析报告页（Agent工作流实时可视化）
&gt; - 设置页
&gt; - 完整的Pinia状态管理
&gt; - SSE流式输出集成
&gt; 
&gt; **Estimated Effort**: Medium
&gt; **Parallel Execution**: YES - 5 waves
&gt; **Critical Path**: 前端基础 → 核心页面 → K线看板 → 工作流可视化 → 集成优化

---

## Context

### Original Request
基于Phase 3完成的Agent工作流，实现优雅美观的前端界面。

### Key Decisions (from Draft)
- **核心框架**: Vue 3.5.32 + TypeScript（仅TypeScript，不使用JavaScript） + Vite 8+ + Pinia
- **UI组件**: Tailwind CSS v4 + Lightweight Charts + shadcn-vue（备选）
- **其他工具**: @langchain/vue@0.2.0（SSE流式输出）+ ECharts 5.5+（备选）+ Playwright（E2E测试）

### Research Findings (2026年4月最新)
- **Vue 3.5.32**: 最新稳定版
- **Vite 8+**: 集成Rolldown，构建更快
- **Pinia**: 官方推荐，Vuex已维护模式
- **Tailwind CSS v4**: Oxide引擎，性能更好
- **Lightweight Charts**: TradingView官方K线图库

---

## Work Objectives

### Core Objective
构建优雅美观、功能完整的前端界面，提供股票搜索、K线看板、Agent工作流可视化、分析报告展示等功能。

### Concrete Deliverables
- [ ] 页面路由配置（Vue Router）
- [ ] Pinia stores设计（stock、analysis、settings）
- [ ] 布局组件（Header、Sidebar、Footer）
- [ ] 首页/股票搜索页
- [ ] 股票详情页框架
- [ ] 分析报告页框架
- [ ] 设置页
- [ ] Lightweight Charts集成与K线看板
- [ ] SSE流式输出集成
- [ ] Agent工作流状态可视化
- [ ] AHP权重可视化（饼图/雷达图）
- [ ] 响应式适配
- [ ] 前后端联调

### Definition of Done
- [ ] `npm run build` → 成功
- [ ] `npm run dev` → 能正常访问首页
- [ ] 能搜索股票并查看详情页
- [ ] K线看板能正常渲染
- [ ] 能启动Agent分析并实时查看输出
- [ ] 响应式适配移动端和桌面端

### Must Have
- 4个核心页面（首页、详情、报告、设置）
- 仿TradingView风格K线看板（Lightweight Charts）
- Agent工作流执行状态展示
- SSE实时流式输出
- AHP权重可视化
- Pinia状态管理
- 响应式设计

### Must NOT Have (Guardrails)
- 不过早添加过度复杂的UI动画
- 不实现非核心功能（如用户系统、收藏等）
- 不过度设计，保持简洁实用

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: YES (from Phase 1)
- **Automated tests**: YES (Tests-after)
- **Framework**: vitest (前端TypeScript) + Playwright (E2E)
- **Agent-Executed QA**: MANDATORY for all tasks

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately - 前端基础):
├── Task 1: 页面路由配置
├── Task 2: Pinia stores设计
├── Task 3: 布局组件（Header、Sidebar、Footer）
└── Task 4: 基础UI组件库集成

Wave 2 (After Wave 1 - 核心页面):
├── Task 5: 首页/搜索页
├── Task 6: 股票详情页框架
├── Task 7: 分析报告页框架
└── Task 8: 设置页

Wave 3 (After Wave 2 - K线看板):
├── Task 9: Lightweight Charts集成
├── Task 10: K线数据渲染
├── Task 11: 技术指标叠加
└── Task 12: 交互功能实现

Wave 4 (After Wave 3 - 工作流可视化):
├── Task 13: SSE流式输出集成
├── Task 14: Agent工作流状态组件
├── Task 15: 报告渲染组件
└── Task 16: AHP可视化

Wave 5 (After All - 集成与优化):
├── Task 17: 前后端联调
├── Task 18: 响应式适配
├── Task 19: 性能优化
└── Task 20: E2E测试
```

### Dependency Matrix

- **1-4**: - - 5-8, 1
- **5-8**: 1-4 - 9-12, 2
- **9-12**: 5-8 - 13-16, 3
- **13-16**: 9-12 - 17-20, 4
- **17-20**: 13-16 - Final, 5

### Agent Dispatch Summary

- **1**: **4** - T1-T4 → `quick`
- **2**: **4** - T5-T8 → `quick`
- **3**: **4** - T9-T12 → `visual-engineering`
- **4**: **4** - T13-T16 → `quick`
- **5**: **4** - T17-T20 → `quick`

---

## TODOs

- [ ] 1. 页面路由配置

  **What to do**:
  - 配置Vue Router
  - 定义路由：/（首页）、/stock/:symbol（详情）、/analysis/:symbol（报告）、/settings（设置）
  - 配置路由守卫

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 2, 3, 4)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: None

  **Commit**: YES
  - Message: `feat: configure Vue Router`

---

- [ ] 2. Pinia stores设计

  **What to do**:
  - 创建useStockStore（当前股票、K线数据、指标数据）
  - 创建useAnalysisStore（分析状态、报告、最终得分）
  - 创建useSettingsStore（用户设置、Token配置）
  - 使用localStorage持久化设置

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 1, 3, 4)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: None

  **Commit**: YES
  - Message: `feat: design Pinia stores`

---

- [ ] 3. 布局组件（Header、Sidebar、Footer）

  **What to do**:
  - 创建Header组件（logo、导航、用户菜单）
  - 创建Sidebar组件（菜单导航）
  - 创建Footer组件（版权、链接）
  - 创建MainLayout布局组件

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 1, 2, 4)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: None

  **Commit**: YES
  - Message: `feat: implement layout components`

---

- [ ] 4. 基础UI组件库集成

  **What to do**:
  - 集成Tailwind CSS v4
  - （可选）集成shadcn-vue组件库
  - 创建基础UI组件（Button、Input、Card等）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 1, 2, 3)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: None

  **Commit**: YES
  - Message: `feat: integrate UI component library`

---

- [ ] 5. 首页/搜索页

  **What to do**:
  - 创建HomeView
  - 实现股票搜索功能（代码/名称）
  - 展示热门股票
  - 展示最近查看历史

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 6, 7, 8)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Commit**: YES
  - Message: `feat: implement home/search page`

---

- [ ] 6. 股票详情页框架

  **What to do**:
  - 创建StockDetailView
  - 展示股票基本信息（现价、涨跌幅等）
  - 集成K线看板组件占位
  - 添加"开始分析"按钮

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5, 7, 8)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Commit**: YES
  - Message: `feat: implement stock detail page skeleton`

---

- [ ] 7. 分析报告页框架

  **What to do**:
  - 创建AnalysisReportView
  - 设计报告页布局
  - 添加各分析师报告展示区域
  - 添加AHP权重可视化区域
  - 添加最终得分和操作建议区域

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5, 6, 8)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Commit**: YES
  - Message: `feat: implement analysis report page skeleton`

---

- [ ] 8. 设置页

  **What to do**:
  - 创建SettingsView
  - 实现数据源配置（Tushare Token，预留AKShare/JQData）
  - 实现LLM提供商配置（API Key）
  - 实现MCP搜索工具配置（Exa/Tavily）
  - 实现外观设置（主题、字体等）
  - 使用localStorage保存设置

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5, 6, 7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Commit**: YES
  - Message: `feat: implement settings page`

---

- [ ] 9. Lightweight Charts集成

  **What to do**:
  - 安装lightweight-charts依赖
  - 创建KlineChart组件
  - 初始化图表容器
  - 配置图表样式（仿TradingView风格）

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 10, 11, 12)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 5, 6, 7, 8

  **Commit**: YES
  - Message: `feat: integrate Lightweight Charts`

---

- [ ] 10. K线数据渲染

  **What to do**:
  - 实现蜡烛图数据渲染
  - 实现成交量柱状图渲染
  - 实现数据更新逻辑
  - 实现时间轴格式化

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 9, 11, 12)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 5, 6, 7, 8

  **Commit**: YES
  - Message: `feat: render K-line data`

---

- [ ] 11. 技术指标叠加

  **What to do**:
  - 实现MA线叠加
  - 实现BOLL带叠加
  - 实现副图指标（KDJ、RSI、MACD等）
  - 实现指标切换功能

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 9, 10, 12)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 5, 6, 7, 8

  **Commit**: YES
  - Message: `feat: add technical indicators overlay`

---

- [ ] 12. 交互功能实现

  **What to do**:
  - 实现缩放和平移
  - 实现十字光标
  - 实现tooltip
  - 实现K线周期切换（日K/周K/月K）

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 9, 10, 11)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 13, 14, 15, 16, 17, 18, 19, 20
  - **Blocked By**: Tasks 5, 6, 7, 8

  **Commit**: YES
  - Message: `feat: implement interactive features`

---

- [ ] 13. SSE流式输出集成

  **What to do**:
  - 集成@langchain/vue或原生EventSource
  - 创建useAnalysis composable
  - 实现SSE连接管理
  - 实现消息解析和状态更新

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 14, 15, 16)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 17, 18, 19, 20
  - **Blocked By**: Tasks 9, 10, 11, 12

  **Commit**: YES
  - Message: `feat: integrate SSE streaming output`

---

- [ ] 14. Agent工作流状态组件

  **What to do**:
  - 创建AgentWorkflowStatus组件
  - 展示各Agent状态（等待/执行中/完成）
  - 展示执行进度条
  - 展示实时日志

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 13, 15, 16)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 17, 18, 19, 20
  - **Blocked By**: Tasks 9, 10, 11, 12

  **Commit**: YES
  - Message: `feat: implement Agent workflow status component`

---

- [ ] 15. 报告渲染组件

  **What to do**:
  - 创建MarkdownReport组件
  - 支持Markdown渲染（代码高亮、表格等）
  - 实现各分析师报告展示
  - 实现最终报告展示

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 13, 14, 16)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 17, 18, 19, 20
  - **Blocked By**: Tasks 9, 10, 11, 12

  **Commit**: YES
  - Message: `feat: implement report rendering component`

---

- [ ] 16. AHP可视化

  **What to do**:
  - 集成ECharts或使用原生Canvas/SVG
  - 创建AHPWeightChart组件
  - 实现权重饼图
  - 实现权重雷达图
  - 实现最终得分展示

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 13, 14, 15)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 17, 18, 19, 20
  - **Blocked By**: Tasks 9, 10, 11, 12

  **Commit**: YES
  - Message: `feat: add AHP visualization`

---

(剩余任务17-20：前后端联调、响应式适配、性能优化、E2E测试，请参考前面阶段类似任务格式)

---

---

## Final Verification Wave

- [ ] F1. **Plan Compliance Audit** — `oracle`
- [ ] F2. **Code Quality Review** — `unspecified-high`
- [ ] F3. **Real Manual QA** — `unspecified-high` (+ Playwright)
- [ ] F4. **Scope Fidelity Check** — `deep`

---

## Commit Strategy

- **1**: `feat: configure Vue Router`
- **2**: `feat: design Pinia stores`
- **3**: `feat: implement layout components`
- **4**: `feat: integrate UI component library`
- **5**: `feat: implement home/search page`
- **6**: `feat: implement stock detail page skeleton`
- **7**: `feat: implement analysis report page skeleton`
- **8**: `feat: implement settings page`
- **9**: `feat: integrate Lightweight Charts`
- **10**: `feat: render K-line data`
- **11**: `feat: add technical indicators overlay`
- **12**: `feat: implement interactive features`
- **13**: `feat: integrate SSE streaming output`
- **14**: `feat: implement Agent workflow status component`
- **15**: `feat: implement report rendering component`
- **16**: `feat: add AHP visualization`
- **17**: `feat: frontend-backend integration`
- **18**: `feat: responsive design`
- **19**: `perf: performance optimization`
- **20**: `test: add E2E tests`

---

## Success Criteria

### Verification Commands
```bash
cd frontend &amp;&amp; npm install &amp;&amp; npm run build  # Expected: build successful
cd frontend &amp;&amp; npm run dev  # Expected: dev server starts at http://localhost:5173
```

### Final Checklist
- [ ] 所有页面实现完成
- [ ] K线看板正常工作
- [ ] Agent工作流实时可视化
- [ ] 前后端联调成功
- [ ] 响应式适配完成
