# Draft: 奕策（YiCe）Phase 3: Agent团队开发

## 阶段概述
基于Phase 2完成的数据源和技术指标计算，本阶段将实现核心的Agent工作流。

## 研究回顾

### TradingAgents架构参考
- 49.8k Stars的成功项目
- 分析师团队 → 多空辩论 → 风险控制 → 交易决策
- 使用LangGraph构建
- 支持多LLM提供商

### AHP层次分析法
- 将复杂问题层次化：目标-准则-指标
- 1-9标度将专家判断数值化
- 一致性检验CR=CI/RI&lt;0.1即可接受

### LangGraph最新特性
- langgraph==1.1.6（2026-04-03）
- 持久化执行、人在回路
- 全面内存管理
- 增强的执行信息

## Phase 3 目标

### 核心Agent团队
1. **技术面分析师Agent**
   - 输入：K线数据、成交量、技术指标
   - 输出：技术面分析报告（Markdown）+ 1-9多空标度
   - 分析内容：趋势判断、支撑阻力、指标信号

2. **基本面分析师Agent**
   - 输入：财务报表、公司信息、行业数据
   - 输出：基本面分析报告（Markdown）+ 1-9多空标度
   - 分析内容：估值、成长性、盈利能力、财务健康

3. **消息面分析师Agent**
   - 输入：最新资讯（Exa/Tavily MCP搜索）
   - 输出：消息面分析报告（Markdown）+ 1-9多空标度
   - 分析内容：利好/利空消息、事件影响、市场反应

4. **情绪面分析师Agent**
   - 输入：（预留接口，后期社交媒体爬虫）
   - 输出：情绪面分析报告（Markdown）+ 1-9多空标度
   - 初期：基于消息面情绪分析，或简化处理

5. **宏观经济/市场分析师Agent**
   - 输入：宏观经济数据、市场趋势资讯
   - 输出：技术面/基本面/消息面/情绪面的权重分配
   - 分析内容：当前市场环境、主导风格、板块轮动

6. **AHP决策引擎**
   - 输入：各分析师的1-9标度 + 权重分配
   - 输出：最终综合得分
   - 实现：层次分析法计算

7. **风险控制交易员Agent**
   - 输入：综合得分 + 各分析报告
   - 输出：总结报告 + 具体交易操作建议
   - 内容：风险提示、仓位建议、操作策略

### LangGraph工作流设计
```
[数据获取] → [指标计算] → [并行分析师团队] → [宏观分析师赋权] → [AHP计算] → [风控交易员] → [最终报告]
                        ↓
                [技术面][基本面][消息面][情绪面]
```

### 技术决策
- **LLM集成**：支持多种提供商（OpenAI、Anthropic、DeepSeek等）
- **结构化输出**：使用Pydantic模型确保输出格式一致
- **工作流持久化**：LangGraph checkpoint保存执行状态
- **人在回路**：关键决策点支持人工干预（可选）

### 必须实现
- 4个基础分析师Agent（技术面、基本面、消息面、情绪面）
- 宏观分析师Agent（权重分配）
- AHP决策引擎
- 风控交易员Agent
- 完整的LangGraph工作流
- Markdown格式报告生成

### 暂不深入
- Agent工作流的复杂优化（用户明确表示前期可调整）
- 社交媒体情绪分析（后期付费功能）
- 实盘交易接口

## 任务分解

### Wave 1: 基础Agent框架
1. Agent基类设计
2. LLM集成模块
3. 结构化输出模型定义
4. Prompt模板系统

### Wave 2: 分析师Agent开发
5. 技术面分析师Agent
6. 基本面分析师Agent
7. 消息面分析师Agent（含MCP搜索集成）
8. 情绪面分析师Agent（简化版）

### Wave 3: 决策与风控
9. 宏观经济/市场分析师Agent
10. AHP决策引擎实现
11. 风险控制交易员Agent
12. 报告生成模块

### Wave 4: LangGraph工作流
13. State定义与管理
14. Graph节点设计
15. 边与条件逻辑
16. Checkpoint配置

### Wave 5: 集成测试
17. 端到端工作流测试
18. 输出质量验证
19. 错误处理完善
20. 文档更新

## 关键技术点

### 结构化输出模型
```python
from pydantic import BaseModel, Field
from typing import Literal

class AnalysisReport(BaseModel):
    report: str = Field(description="Markdown格式分析报告")
    sentiment_score: int = Field(description="1-9多空标度，1=极度看空，9=极度看多", ge=1, le=9)
    key_points: list[str] = Field(description="关键观点列表")

class WeightAssignment(BaseModel):
    technical_weight: float = Field(description="技术面权重", ge=0, le=1)
    fundamental_weight: float = Field(description="基本面权重", ge=0, le=1)
    news_weight: float = Field(description="消息面权重", ge=0, le=1)
    sentiment_weight: float = Field(description="情绪面权重", ge=0, le=1)
    
    @model_validator(mode='after')
    def check_sum(self):
        total = self.technical_weight + self.fundamental_weight + self.news_weight + self.sentiment_weight
        assert abs(total - 1.0) &lt; 0.001, "权重之和必须为1"
        return self
```

### AHP计算实现
```python
class AHPEngine:
    def calculate_final_score(self, 
                             technical_score: int,
                             fundamental_score: int, 
                             news_score: int,
                             sentiment_score: int,
                             weights: WeightAssignment) -&gt; float:
        # 归一化分数到0-1
        tech_norm = (technical_score - 1) / 8
        fund_norm = (fundamental_score - 1) / 8
        news_norm = (news_score - 1) / 8
        sent_norm = (sentiment_score - 1) / 8
        
        # 加权求和
        final_score = (
            tech_norm * weights.technical_weight +
            fund_norm * weights.fundamental_weight +
            news_norm * weights.news_weight +
            sent_norm * weights.sentiment_weight
        )
        
        return final_score
```

### LangGraph State设计
```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    symbol: str  # 股票代码
    kline_data: pd.DataFrame
    indicator_data: dict
    fundamental_data: dict
    news_data: list
    technical_report: AnalysisReport
    fundamental_report: AnalysisReport
    news_report: AnalysisReport
    sentiment_report: AnalysisReport
    weights: WeightAssignment
    final_score: float
    final_report: str
```

## 依赖关系
- 依赖Phase 2完成的数据源和指标计算
- 为Phase 4（前端）提供API接口
