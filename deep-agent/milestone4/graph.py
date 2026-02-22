from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.planning_node import planning_node
from agent.worker_node import execute_node
from agent.synthesis_node import synthesis_node


graph = StateGraph(AgentState)

# ---- Nodes ----
graph.add_node("plan", planning_node)
graph.add_node("execute", execute_node)
graph.add_node("synthesize", synthesis_node)

# ---- Entry ----
graph.set_entry_point("plan")

# ---- Flow ----
graph.add_edge("plan", "execute")


def route_after_execute(state):
    if state["completed"]:
        return "synthesize"
    return "execute"


graph.add_conditional_edges(
    "execute",
    route_after_execute,
    {
        "execute": "execute",
        "synthesize": "synthesize"
    }
)

graph.add_edge("synthesize", END)

app = graph.compile()


