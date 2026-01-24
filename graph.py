from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from agent.state import AgentState
from agent.planner import write_todos
from agent.filesystem import ls, write_file, read_file, edit_file
from agent.react_loop import agent_runnable


# -------------------------------------------------
# Register all tools (Milestone-1 + Milestone-2)
# -------------------------------------------------
tools = [
    write_todos,   # Milestone-1: Task planning
    ls,            # Milestone-2: List files
    write_file,    # Milestone-2: Write file
    read_file,     # Milestone-2: Read file
    edit_file      # Milestone-2: Edit file
]


# -------------------------------------------------
# Create LangGraph StateGraph
# -------------------------------------------------
graph = StateGraph(state_schema=AgentState)


# -------------------------------------------------
# Agent node (ReAct reasoning loop)
# -------------------------------------------------
graph.add_node("agent", agent_runnable)


# -------------------------------------------------
# Tool execution node
# -------------------------------------------------
graph.add_node("tools", ToolNode(tools))


# -------------------------------------------------
# Graph control flow
# -------------------------------------------------
# Agent decides → tools execute → back to agent
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

# Agent finishes → END
# graph.add_edge("agent", END)  <-- Implicitly handled by tools_condition


# -------------------------------------------------
# Entry point
# -------------------------------------------------
graph.set_entry_point("agent")


# -------------------------------------------------
# Compile graph
# -------------------------------------------------
app = graph.compile()
