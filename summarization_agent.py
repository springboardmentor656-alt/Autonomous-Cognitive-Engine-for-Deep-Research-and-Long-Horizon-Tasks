from langgraph.graph import StateGraph, END
from langsmith import traceable

from agent_state import AgentState
from vfs import write_file


@traceable(name="summarization_node")
def summarization_node(state: AgentState) -> AgentState:
    text = state["messages"][-1]

    summary = """
• Insight from summary
• Important extracted idea
• Final takeaway
"""

    write_file(state, "todo_1_summary.txt", summary)

    state["messages"].append("Summary written to file by sub-agent.")
    state["done"] = True
    return state


builder = StateGraph(AgentState)
builder.add_node("summarization", summarization_node)
builder.set_entry_point("summarization")
builder.add_edge("summarization", END)

summarization_graph = builder.compile()
