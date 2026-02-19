from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import plan_node, execute_node, synthesize_node, orchestrator_node


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("plan", plan_node)
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("execute", execute_node)
    graph.add_node("synthesize", synthesize_node)

    graph.set_entry_point("plan")

    graph.add_edge("plan", "orchestrator")

    graph.add_conditional_edges(
        "orchestrator",
        lambda state: state["next_action"],
        {
            "execute": "execute",
            "synthesize": "synthesize",
        },
    )

    graph.add_edge("execute", "orchestrator")
    graph.add_edge("synthesize", END)

    return graph.compile()

