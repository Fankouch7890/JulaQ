import os
from typing import Sequence, Dict, Any, Union
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from langgraph.prebuilt import ToolNode

from agent.tools import ALL_TOOLS

SYSTEM_PROMPT = """أنت JulaQ (جولاق)، مساعد ذكي مخصص للتحكم بالروبوتات والأتمتة في شبكة Fabric.
إليك التوجيهات:
1. تجيب باللغة العربية بدقة ووضوح وبطريقة مساعدة ومحترفة.
2. تستخدم أدوات التحكم بالروبوتات المتاحة عند طلب المستخدم تحريك روبوت، إيقافه، جلب حالته، أو تنفيذ إجراءات عليه.
3. إذا طلب المستخدم أمراً يتطلب أداة، قم باستدعاء الأداة المناسبة باسم الروبوت المعطى.
"""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    last_message = messages[-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    return END

def create_julaq_agent(model_name: str = "gpt-4o-mini", temperature: float = 0.7):
    """
    بناء وإرجاع رسم بياني للوكيل الذكي JulaQ باستخدام LangGraph.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        llm = ChatOpenAI(model=model_name, temperature=temperature, api_key="placeholder")
    else:
        llm = ChatOpenAI(model=model_name, temperature=temperature)

    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    async def call_model(state: AgentState) -> Dict[str, Any]:
        messages = state["messages"]
        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    tool_node = ToolNode(ALL_TOOLS)

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, ["tools", END])
    workflow.add_edge("tools", "agent")

    return workflow.compile()
