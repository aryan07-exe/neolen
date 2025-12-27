from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.orchestrator import orchestrator_node
from app.agents.tracking import tracking_node
from app.agents.knowledge import knowledge_node
from app.agents.analytics import analytics_node
from app.agents.insight import insight_node

def route_orchestrator(state: AgentState):
    intent = state["intent"]
    if intent == "TRACK":
        return "tracking"
    elif intent == "ANALYTICS":
        return "analytics"
    else:
        return "knowledge"

workflow = StateGraph(AgentState)

workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("tracking", tracking_node)
workflow.add_node("knowledge", knowledge_node)
workflow.add_node("analytics", analytics_node)
workflow.add_node("insight", insight_node)

workflow.set_entry_point("orchestrator")

workflow.add_conditional_edges(
    "orchestrator",
    route_orchestrator,
    {
        "tracking": "tracking",
        "analytics": "analytics",
        "knowledge": "knowledge"
    }
)

workflow.add_edge("analytics", "insight")
workflow.add_edge("tracking", END)
workflow.add_edge("knowledge", END)
workflow.add_edge("insight", END)

graph = workflow.compile()
