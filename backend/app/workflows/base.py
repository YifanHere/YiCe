from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class BaseState(TypedDict):
    """基础工作流状态，包含消息和其他公共字段"""
    messages: Annotated[Sequence[BaseMessage], add_messages]


class BaseWorkflow:
    """LangGraph工作流基类"""
    
    def __init__(self):
        self.graph = None
        self._build_graph()
    
    def _build_graph(self):
        """构建图结构，子类需要重写此方法"""
        workflow = StateGraph(BaseState)
        
        # 基础框架：空的节点和边，子类可在此基础上扩展
        workflow.add_node("__start__", self._dummy_node)
        
        # 初始边
        workflow.add_edge(START, "__start__")
        workflow.add_edge("__start__", END)
        
        self.graph = workflow.compile()
    
    def _dummy_node(self, state: BaseState) -> BaseState:
        """
        空节点，仅用于占位
        
        Args:
            state: 当前状态
            
        Returns:
            未修改的状态
        """
        return state
    
    def invoke(self, *args, **kwargs):
        """调用工作流，代理到graph.invoke"""
        return self.graph.invoke(*args, **kwargs)
    
    async def ainvoke(self, *args, **kwargs):
        """异步调用工作流，代理到graph.ainvoke"""
        return await self.graph.ainvoke(*args, **kwargs)
    
    def stream(self, *args, **kwargs):
        """流式调用工作流，代理到graph.stream"""
        return self.graph.stream(*args, **kwargs)
    
    async def astream(self, *args, **kwargs):
        """异步流式调用工作流，代理到graph.astream"""
        return self.graph.astream(*args, **kwargs)
