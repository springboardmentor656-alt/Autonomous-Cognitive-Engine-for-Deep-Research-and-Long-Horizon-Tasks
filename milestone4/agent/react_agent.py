from langgraph.graph import StateGraph, END
from agent.state import AgentState
from tools.write_todos import write_todos
from tools.vfs import write_file, read_file
from tools.task import task


# =====================================================
# ENTRY NODE
# =====================================================
def react_entry(state: AgentState):

    user_text = state["messages"][-1]["content"]

    # Decide if complex task
    if "article" in user_text.lower() or "research" in user_text.lower():

        write_file.invoke({
            "filename": "notes.txt",
            "content": user_text,
            "state": state
        })

        state["needs_read"] = True
        return state

    # Simple task → directly create TODOs
    state["todos"] = write_todos.invoke(user_text)
    state["needs_read"] = False

    return state


# =====================================================
# READ NOTES NODE
# =====================================================
def read_notes(state: AgentState):

    notes = read_file.invoke({
        "filename": "notes.txt",
        "state": state
    })

    # Delegate summarization to sub-agent
    summary = task.invoke({
        "agent_name": "summarize",
        "input_text": notes
    })

    # Store summary
    write_file.invoke({
        "filename": "summary.txt",
        "content": summary,
        "state": state
    })

    # Generate TODOs from summary
    state["todos"] = write_todos.invoke(summary)

    # Reset flag
    state["needs_read"] = False

    return state


# =====================================================
# EXECUTE PLAN NODE  ⭐ NEW FOR MILESTONE-4
# =====================================================
def execute_plan(state: AgentState):

    plan = state.get("todos", [])

    if not plan:
        state["report"] = "No plan found to execute."
        return state

    plan_text = "\n".join(plan)

    execution_prompt = f"""
You are a research writer.

Using the plan below, write a FULL research report.

PLAN:
{plan_text}

Instructions:
- Write a proper introduction
- Expand each point into a paragraph
- Explain concepts clearly
- Add examples if useful
- Write a short conclusion

Return ONLY the research report text.
Do NOT return bullet points.
Do NOT repeat the plan.
"""

    report = task.invoke({
        "agent_name": "summarize",
        "input_text": execution_prompt
    })

    state["report"] = report
    return state



# =====================================================
# ROUTER
# =====================================================
def router(state: AgentState):

    if state.get("needs_read"):
        return "read_notes"

    return "execute_plan"


# =====================================================
# FINAL NODE
# =====================================================
def final_answer(state: AgentState):

    # If report exists → show report
    report = state.get("report")

# If no report, generate from todos

    if not report and state.get("todos"):
        plan_text = "\n".join(state["todos"])
    report = task.invoke({
        "agent_name": "summarize",
        "input_text": f"Write a research report based on:\n{plan_text}"
    })


    if report:
        state["final_output"] = "FINAL RESEARCH REPORT:\n\n" + report
        return state

    # Fallback → show plan
    todos = state.get("todos", [])

    if not todos:
        state["final_output"] = "No output generated."
        return state

    formatted = "FINAL RESEARCH PLAN:\n\n"
    for t in todos:
        formatted += f"- {t}\n"

    state["final_output"] = formatted
    return state


# =====================================================
# BUILD GRAPH
# =====================================================
graph = StateGraph(AgentState)

graph.add_node("react_entry", react_entry)
graph.add_node("read_notes", read_notes)
graph.add_node("execute_plan", execute_plan)
graph.add_node("final_answer", final_answer)

graph.set_entry_point("react_entry")
graph.add_conditional_edges("react_entry", router)

# ⭐ CORRECT FLOW FOR MILESTONE-4
graph.add_edge("read_notes", "execute_plan")
graph.add_edge("execute_plan", "final_answer")
graph.add_edge("final_answer", END)

app = graph.compile()
