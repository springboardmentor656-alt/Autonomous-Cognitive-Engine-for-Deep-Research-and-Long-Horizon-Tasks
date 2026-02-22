from langgraph.graph import StateGraph, END
from planner import planning_node
from orchestrator import orchestrator_node
from tools.executor import executor_node
from finalizer import finalize_report


def build_master_agent():

    graph = StateGraph(dict)

    graph.add_node("planning", planning_node)
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("executor", executor_node)
    graph.add_node("finalizer", finalize_report)

    graph.set_entry_point("planning")

    graph.add_edge("planning", "orchestrator")

    graph.add_conditional_edges(
        "orchestrator",
        lambda state: state["next_action"],
        {
            "execute": "executor",
            "finalize": "finalizer"
        }
    )

    graph.add_edge("executor", "orchestrator")
    graph.add_edge("finalizer", END)

    return graph.compile()
