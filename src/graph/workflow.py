from langgraph.graph import StateGraph, END, START
import sys
import os

# Ensure the graph can see the state and nodes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import AgentState
from nodes import planner_node, research_node, writer_node, reflector_node

# 1. Create the Graph
builder = StateGraph(AgentState)

# 2. Add Nodes
builder.add_node("planner", planner_node)
builder.add_node("researcher", research_node)
builder.add_node("writer", writer_node)
builder.add_node("reflector", reflector_node)

# 3. Define Edges
builder.add_edge(START, "planner")
builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "writer")
builder.add_edge("writer", "reflector")

# 4. Define Conditional Logic (The Loop)
def should_continue(state: AgentState):
    # If approved or we've tried 3 times, stop.
    if "APPROVED" in state.get("critique", "").upper() or state.get("revision_count", 0) >= 3:
        return "end"
    return "continue"


builder.add_conditional_edges(
    "reflector",
    should_continue,
    {
        "end": END,
        "continue": "researcher"
    }
)

app = builder.compile()