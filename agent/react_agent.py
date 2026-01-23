from langgraph.graph import StateGraph, END
from agent.state import AgentState
from tools.write_todos import write_todos
from tools.vfs import write_file, read_file

# ---------- ENTRY ----------
def react_entry(state: AgentState):
    user_text = state["messages"][-1]["content"]

    # Agent REASONING (not python length hack)
    if "article" in user_text.lower() or "research" in user_text.lower():
        write_file.invoke({
            "filename": "notes.txt",
            "content": user_text,
            "state": state
        })
        state["needs_read"] = True
        return state

    # Short/simple task
    state["todos"] = write_todos.invoke(user_text)
    state["needs_read"] = False
    return state

# ---------- READ NOTES ----------
def read_notes(state: AgentState):
    notes = read_file.invoke({
        "filename": "notes.txt",
        "state": state
    })

    state["todos"] = write_todos.invoke(notes)
    return state

# ---------- ROUTER ----------
def router(state: AgentState):
    if state.get("needs_read"):
        return "read_notes"
    return END

# ---------- GRAPH ----------
graph = StateGraph(AgentState)

graph.add_node("react_entry", react_entry)
graph.add_node("read_notes", read_notes)

graph.set_entry_point("react_entry")
graph.add_conditional_edges("react_entry", router)
graph.add_edge("read_notes", END)

app = graph.compile()