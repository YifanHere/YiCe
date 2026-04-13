# Draft: 奕策（YiCe）Phase 4: 前端界面开发

## 阶段概述
基于Phase 3完成的Agent工作流，本阶段将实现优雅美观的前端界面。

## 前端技术栈（2026年4月最新）

### 核心框架
- **Vue 3.5.32** - 最新稳定版
- **TypeScript** - 类型安全
- **Vite 8+** - 构建工具（Rolldown集成）
- **Pinia** - 状态管理（Vuex已维护模式）
- **Vue Router** - 路由管理

### UI组件与样式
- **Tailwind CSS v4** - CSS框架（Oxide引擎）
- **UnoCSS** - 备选方案（原子化CSS）
- **Lightweight Charts** - TradingView官方K线图库
- **shadcn-vue** - 组件库备选

### 其他工具
- **@langchain/vue@0.2.0** - LangChain Vue集成，支持SSE流式输出
- **ECharts 5.5+** - 数据可视化备选
- **Playwright** - E2E测试

## Phase 4 目标

### 核心页面
1. **首页/股票搜索页**
   - 股票代码/名称搜索
   - 热门股票推荐
   - 最近查看历史

2. **股票详情页**
   - 仿TradingView风格K线看板
   - 技术指标叠加（主图/副图）
   - 成交量显示
   - 基础信息展示（现价、涨跌幅等）

3. **分析报告页**
   - Agent工作流执行状态展示
   - 实时流式输出（SSE）
   - 各分析师报告展示
   - AHP权重可视化
   - 最终综合得分展示
   - 风控交易员建议

4. **设置页**
   - 数据源配置（Tushare Token，预留AKShare/JQData接口）
   - LLM提供商配置（API Key）
   - MCP搜索工具配置（Exa/Tavily）
   - 外观设置（主题、字体等）

### 核心功能模块
1. **K线看板组件**
   - 基于Lightweight Charts实现
   - 支持日K/周K/月K切换
   - 支持技术指标叠加
   - 缩放、平移交互
   - 十字光标、tooltip

2. **Agent工作流可视化**
   - 工作流执行进度条
   - 各Agent状态（等待/执行中/完成）
   - 实时输出日志
   - 流式报告渲染

3. **数据可视化**
   - AHP权重饼图/雷达图
   - 技术指标图表
   - 历史得分趋势（预留）

4. **状态管理**
   - 当前选中股票
   - 分析报告缓存
   - 用户设置持久化
   - 工作流状态

## 任务分解

### Wave 1: 前端基础
1. 页面路由配置
2. Pinia stores设计
3. 布局组件（Header、Sidebar、Footer）
4. 基础UI组件库集成

### Wave 2: 核心页面
5. 首页/搜索页
6. 股票详情页框架
7. 分析报告页框架
8. 设置页

### Wave 3: K线看板
9. Lightweight Charts集成
10. K线数据渲染
11. 技术指标叠加
12. 交互功能实现

### Wave 4: 工作流可视化
13. SSE流式输出集成
14. Agent工作流状态组件
15. 报告渲染组件
16. AHP可视化

### Wave 5: 集成与优化
17. 前后端联调
18. 响应式适配
19. 性能优化
20. E2E测试

## 关键技术点

### K线看板组件设计
```vue
&lt;template&gt;
  &lt;div ref="chartContainer" class="chart-container"&gt;&lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
import { ref, onMounted, watch } from 'vue'
import { createChart, IChartApi, ISeriesApi } from 'lightweight-charts'
import { useStockStore } from '@/stores/stock'

const chartContainer = ref&lt;HTMLDivElement&gt;()
const stockStore = useStockStore()

let chart: IChartApi | null = null
let candlestickSeries: ISeriesApi&lt;'Candlestick'&gt; | null = null
let volumeSeries: ISeriesApi&lt;'Histogram'&gt; | null = null

onMounted(() =&gt; {
  if (!chartContainer.value) return
  
  chart = createChart(chartContainer.value, {
    layout: {
      background: { type: 'solid', color: '#ffffff' },
      textColor: '#333',
    },
    grid: {
      vertLines: { color: '#f0f0f0' },
      horzLines: { color: '#f0f0f0' },
    },
  })
  
  candlestickSeries = chart.addCandlestickSeries()
  volumeSeries = chart.addHistogramSeries({
    priceFormat: {
      type: 'volume',
    },
    priceScaleId: '',
  })
  
  chart.timeScale().fitContent()
})

watch(() =&gt; stockStore.klineData, (data) =&gt; {
  if (!candlestickSeries || !volumeSeries || !data) return
  
  candlestickSeries.setData(data.candles)
  volumeSeries.setData(data.volume)
}, { deep: true })
&lt;/script&gt;
```

### SSE流式输出集成
```typescript
// services/agent.ts
import { useAnalysisStore } from '@/stores/analysis'

export async function startAnalysis(symbol: string) {
  const analysisStore = useAnalysisStore()
  analysisStore.reset()
  analysisStore.setStatus('running')
  
  const eventSource = new EventSource(`/api/analyze/${symbol}/stream`)
  
  eventSource.onmessage = (event) =&gt; {
    const data = JSON.parse(event.data)
    switch (data.type) {
      case 'agent_update':
        analysisStore.updateAgentStatus(data.agent, data.status)
        break
      case 'report_chunk':
        analysisStore.appendReport(data.agent, data.content)
        break
      case 'final_score':
        analysisStore.setFinalScore(data.score)
        break
      case 'complete':
        analysisStore.setStatus('completed')
        eventSource.close()
        break
    }
  }
  
  eventSource.onerror = () =&gt; {
    analysisStore.setStatus('error')
    eventSource.close()
  }
}
```

### Pinia Store设计
```typescript
// stores/stock.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useStockStore = defineStore('stock', () =&gt; {
  const currentSymbol = ref&lt;string&gt;('')
  const klineData = ref&lt;any&gt;(null)
  const indicatorData = ref&lt;any&gt;(null)
  const basicInfo = ref&lt;any&gt;(null)
  
  const isLoading = computed(() =&gt; !klineData.value)
  
  async function fetchStockData(symbol: string) {
    currentSymbol.value = symbol
    // 调用API获取数据
  }
  
  return {
    currentSymbol,
    klineData,
    indicatorData,
    basicInfo,
    isLoading,
    fetchStockData,
  }
})
```

## 依赖关系
- 依赖Phase 3完成的后端API
- 为Phase 5（集成测试）提供完整应用
