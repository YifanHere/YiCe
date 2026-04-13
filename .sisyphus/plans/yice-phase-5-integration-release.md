# 奕策（YiCe）- Phase 5: 集成测试 + 优化 + 发布准备

## TL;DR

&gt; **Quick Summary**: 完成端到端测试、性能优化、文档完善和GitHub开源发布准备
&gt; 
&gt; **Deliverables**:
&gt; - 完整的测试套件（单元+集成+E2E）
&gt; - 性能优化（后端API+前端加载）
&gt; - 完整文档（README、架构、API、部署、贡献指南）
&gt; - GitHub开源发布准备（LICENSE、CONTRIBUTING、Issue/PR模板）
&gt; 
&gt; **Estimated Effort**: Medium
&gt; **Parallel Execution**: YES - 5 waves
&gt; **Critical Path**: 测试框架 → 测试执行 → 性能优化 → 文档撰写 → 发布准备

---

## Context

### Original Request
基于前4个阶段的开发成果，完成端到端测试、性能优化、文档完善和开源发布准备。

### Key Decisions (from Draft)
- **测试框架**: pytest（后端）+ vitest（前端TypeScript）+ Playwright（E2E）
- **文档体系**: README.md + 架构文档 + API文档 + 部署指南 + 贡献指南
- **开源协议**: MIT或Apache-2.0
- **成功标准**: 所有测试通过、性能达标、文档完整、docker compose一键启动

---

## Work Objectives

### Core Objective
完成项目的全面测试、性能优化、文档完善，为GitHub开源发布做好准备。

### Concrete Deliverables
- [ ] 后端pytest测试框架完善
- [ ] 前端vitest测试框架完善
- [ ] Playwright E2E测试配置
- [ ] 完整的测试数据准备
- [ ] 后端单元测试（覆盖率&gt;70%）
- [ ] 前端单元测试（覆盖率&gt;60%）
- [ ] API集成测试
- [ ] Playwright E2E测试
- [ ] 错误场景测试
- [ ] 性能基准测试
- [ ] 后端API响应优化
- [ ] 前端打包优化
- [ ] 缓存策略调优
- [ ] README.md完善（快速开始、功能介绍）
- [ ] 架构设计文档
- [ ] API文档（Swagger/OpenAPI）
- [ ] 部署指南
- [ ] 开发者贡献指南
- [ ] LICENSE文件确认
- [ ] CONTRIBUTING.md
- [ ] GitHub仓库配置
- [ ] Issue/PR模板

### Definition of Done
- [ ] 所有测试通过（后端+前端+E2E）
- [ ] 测试覆盖率达标（后端&gt;70%，前端&gt;60%）
- [ ] `docker compose up` 能一键启动完整应用
- [ ] 用户能在30分钟内完成安装并运行第一次分析
- [ ] 所有文档完整清晰
- [ ] GitHub发布准备就绪

### Must Have
- 完整的测试套件（单元+集成+E2E）
- 性能基准测试
- 完整的文档体系
- GitHub开源发布准备
- Docker compose一键启动

### Must NOT Have (Guardrails)
- 不添加新功能（仅测试、优化、文档）
- 不过度优化（满足基本性能即可）
- 不添加过度复杂的CI/CD（基础GitHub Actions即可）

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: YES
- **Automated tests**: YES (THIS IS THE TEST PHASE)
- **Framework**: pytest + vitest + Playwright
- **Agent-Executed QA**: MANDATORY for all tasks

### QA Policy
This is the final verification phase - ALL tasks are QA-focused.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately - 测试框架搭建):
├── Task 1: 后端pytest测试框架完善
├── Task 2: 前端vitest测试框架完善
├── Task 3: Playwright E2E测试配置
└── Task 4: 测试数据准备

Wave 2 (After Wave 1 - 测试执行):
├── Task 5: 后端单元测试
├── Task 6: 前端单元测试
├── Task 7: API集成测试
├── Task 8: Playwright E2E测试
├── Task 9: 错误场景测试
└── Task 10: 性能基准测试

Wave 3 (After Wave 2 - 性能优化):
├── Task 11: 后端API响应优化
├── Task 12: 数据库查询优化（如需要）
├── Task 13: 前端打包优化
├── Task 14: 图片/资源懒加载
└── Task 15: 缓存策略调优

Wave 4 (After Wave 3 - 文档撰写):
├── Task 16: README.md完善
├── Task 17: 架构设计文档
├── Task 18: API文档（Swagger/OpenAPI）
├── Task 19: 部署指南
└── Task 20: 开发者贡献指南

Wave 5 (After All - 发布准备):
├── Task 21: LICENSE文件确认
├── Task 22: CONTRIBUTING.md
├── Task 23: GitHub仓库配置
├── Task 24: Issue/PR模板
└── Task 25: 最终检查与发布
```

### Dependency Matrix

- **1-4**: - - 5-10, 1
- **5-10**: 1-4 - 11-15, 2
- **11-15**: 5-10 - 16-20, 3
- **16-20**: 11-15 - 21-25, 4
- **21-25**: 16-20 - Final, 5

### Agent Dispatch Summary

- **1**: **4** - T1-T4 → `quick`
- **2**: **6** - T5-T10 → `unspecified-high`
- **3**: **5** - T11-T15 → `quick`
- **4**: **5** - T16-T20 → `writing`
- **5**: **5** - T21-T25 → `quick`

---

## TODOs

- [ ] 1. 后端pytest测试框架完善

  **What to do**:
  - 完善pytest配置（conftest.py）
  - 添加测试fixtures
  - 配置覆盖率报告
  - 添加测试数据工厂

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 2, 3, 4)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
  - **Blocked By**: None

  **Commit**: YES
  - Message: `test:完善后端pytest测试框架`

---

- [ ] 2. 前端vitest测试框架完善

  **What to do**:
  - 完善vitest配置
  - 添加测试setup文件
  - 配置测试覆盖率
  - 添加Vue组件测试工具

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 1, 3, 4)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
  - **Blocked By**: None

  **Commit**: YES
  - Message: `test:完善前端vitest测试框架`

---

- [ ] 3. Playwright E2E测试配置

  **What to do**:
  - 安装Playwright依赖
  - 配置Playwright（playwright.config.ts）
  - 下载浏览器
  - 创建测试基础结构

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 1, 2, 4)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
  - **Blocked By**: None

  **Commit**: YES
  - Message: `test:配置Playwright E2E测试`

---

- [ ] 4. 测试数据准备

  **What to do**:
  - 创建测试用股票数据
  - 创建测试用K线数据
  - 创建测试用财务数据
  - 创建mock API响应

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 1, 2, 3)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
  - **Blocked By**: None

  **Commit**: YES
  - Message: `test:准备测试数据`

---

- [ ] 5. 后端单元测试

  **What to do**:
  - 编写Agent单元测试
  - 编写服务单元测试
  - 编写工具函数单元测试
  - 目标覆盖率：&gt;70%

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 6, 7, 8, 9, 10)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Commit**: YES
  - Message: `test:添加后端单元测试`

---

- [ ] 6. 前端单元测试

  **What to do**:
  - 编写组件单元测试
  - 编写stores单元测试
  - 编写composables单元测试
  - 编写工具函数单元测试
  - 目标覆盖率：&gt;60%

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5, 7, 8, 9, 10)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Commit**: YES
  - Message: `test:添加前端单元测试`

---

- [ ] 7. API集成测试

  **What to do**:
  - 编写数据API集成测试
  - 编写Agent API集成测试
  - 编写分析工作流集成测试
  - 使用testcontainer启动测试环境

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5, 6, 8, 9, 10)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Commit**: YES
  - Message: `test:添加API集成测试`

---

- [ ] 8. Playwright E2E测试

  **What to do**:
  - 编写首页搜索E2E测试
  - 编写股票详情页E2E测试
  - 编写分析工作流E2E测试
  - 编写设置页E2E测试

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5, 6, 7, 9, 10)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Commit**: YES
  - Message: `test:添加Playwright E2E测试`

---

- [ ] 9. 错误场景测试

  **What to do**:
  - 测试Tushare Token无效场景
  - 测试LLM API失败场景
  - 测试网络异常场景
  - 测试无效股票代码场景
  - 验证错误处理和用户提示

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5, 6, 7, 8, 10)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Commit**: YES
  - Message: `test:添加错误场景测试`

---

- [ ] 10. 性能基准测试

  **What to do**:
  - 测试K线数据获取性能
  - 测试指标计算性能
  - 测试Agent分析性能
  - 测试前端加载性能
  - 记录基准数据

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills": []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5, 6, 7, 8, 9)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
  - **Blocked By**: Tasks 1, 2, 3, 4

  **Commit**: YES
  - Message: `test:性能基准测试`

---

(剩余任务11-25：性能优化、文档撰写、发布准备，请参考前面阶段类似任务格式)

---

---

## Final Verification Wave

- [ ] F1. **Plan Compliance Audit** — `oracle`
- [ ] F2. **Code Quality Review** — `unspecified-high`
- [ ] F3. **Real Manual QA** — `unspecified-high` (+ Playwright full E2E)
- [ ] F4. **Scope Fidelity Check** — `deep`

---

## Key Checklists

### 功能完整性
- [ ] Phase 1-4所有功能已实现
- [ ] 核心工作流端到端正常运行
- [ ] 错误处理完善
- [ ] 用户设置持久化

### 代码质量
- [ ] Python代码通过ruff/flake8检查
- [ ] TypeScript代码通过eslint检查（仅TypeScript，不使用JavaScript）
- [ ] 测试覆盖率达到目标（后端&gt;70%，前端&gt;60%）
- [ ] 无console.log/debugger遗留

### 文档
- [ ] README.md包含完整快速开始
- [ ] 架构图已绘制
- [ ] API文档已生成
- [ ] 部署步骤清晰

### 开源准备
- [ ] LICENSE已选择（MIT/Apache-2.0）
- [ ] .gitignore完善
- [ ] 敏感信息已清理
- [ ] 贡献指南已撰写

---

## Commit Strategy

- **1**: `test:完善后端pytest测试框架`
- **2**: `test:完善前端vitest测试框架`
- **3**: `test:配置Playwright E2E测试`
- **4**: `test:准备测试数据`
- **5**: `test:添加后端单元测试`
- **6**: `test:添加前端单元测试`
- **7**: `test:添加API集成测试`
- **8**: `test:添加Playwright E2E测试`
- **9**: `test:添加错误场景测试`
- **10**: `test:性能基准测试`
- **11**: `perf:优化后端API响应`
- **12**: `perf:优化数据库查询`
- **13**: `perf:优化前端打包`
- **14**: `perf:添加图片/资源懒加载`
- **15**: `perf:调优缓存策略`
- **16**: `docs:完善README.md`
- **17**: `docs:撰写架构设计文档`
- **18**: `docs:生成API文档`
- **19**: `docs:撰写部署指南`
- **20**: `docs:撰写开发者贡献指南`
- **21**: `chore:确认LICENSE文件`
- **22**: `chore:添加CONTRIBUTING.md`
- **23**: `chore:配置GitHub仓库`
- **24**: `chore:添加Issue/PR模板`
- **25**: `chore:最终检查与发布准备`

---

## Success Criteria

### Verification Commands
```bash
# 后端测试
cd backend &amp;&amp; uv run pytest --cov=app tests/  # Expected: coverage &gt;70%

# 前端测试
cd frontend &amp;&amp; npm run test:coverage  # Expected: coverage &gt;60%

# E2E测试
cd frontend &amp;&amp; npm run test:e2e  # Expected: all E2E tests pass

# 完整应用启动
docker compose up --build  # Expected: all services start successfully

# 健康检查
curl http://localhost:8000/health  # Expected: {"status": "healthy"}
```

### Final Checklist
- [ ] 所有测试通过
- [ ] 测试覆盖率达标
- [ ] 性能满足预期
- [ ] 文档完整清晰
- [ ] 项目可通过docker compose一键启动
- [ ] 用户能在30分钟内完成安装并运行第一次分析
- [ ] GitHub发布准备就绪
