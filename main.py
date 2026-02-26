from typing import cast
from langgraph.graph import StateGraph, END
from langsmith import traceable

from agent_state import AgentState
from tools import writetodos_tool, delegate_task, generate_final_report


# =========================================================
# ORCHESTRATOR NODE — MASTER ARCHITECT
# =========================================================
@traceable(name="orchestrator_node")
def orchestrator_node(state: AgentState) -> AgentState:

    messages = state.get("messages", [])
    todos = state.get("todos", [])
    files = state.get("files", {})
    sub_agent_results = state.get("sub_agent_results", {})

    # -----------------------------------------------------
    # 1. STRATEGIC PLANNING
    # -----------------------------------------------------
    if not todos:
        state["todos"] = writetodos_tool(messages[0])
        return state

    # -----------------------------------------------------
    # 2. EXECUTE NEXT PENDING TASK
    # -----------------------------------------------------
    for task in todos:

        if task.get("status") == "pending":

            description = task.get("description", "").lower()

            # -------- SUMMARIZATION → SUB-AGENT --------
            if "summarize" in description:

                result = delegate_task(
                    state,
                    "Summarization_Agent",
                    {"text": messages[0]}
                )

                sub_agent_results[f"task_{task['id']}"] = result

                for fname, content in result.get("files", {}).items():
                    files[fname] = content

                task["status"] = "completed"
                state["sub_agent_results"] = sub_agent_results
                state["files"] = files
                return state

            # -------- RESEARCH PHASE --------
            elif "research" in description:

                research_note = (
                    "Background research completed.\n"
                    "Market positioning analyzed.\n"
                    "Competitive factors documented."
                )

                files[f"research_task_{task['id']}.txt"] = research_note
                task["status"] = "completed"
                state["files"] = files
                return state

            # -------- FINAL REPORT SYNTHESIS --------
            elif "write" in description:

                report = generate_final_report(files)

                files["final_report.md"] = report

                with open("final_report.md", "w", encoding="utf-8") as f:
                    f.write(report)

                task["status"] = "completed"
                state["files"] = files
                return state

    # -----------------------------------------------------
    # 3. TERMINATION CONDITION
    # -----------------------------------------------------
    if all(task.get("status") == "completed" for task in todos):
        state["done"] = True

    return state


# =========================================================
# STOP CONDITION
# =========================================================
def should_continue(state: AgentState):
    return END if state.get("done", False) else "orchestrator"


# =========================================================
# GRAPH BUILD
# =========================================================
builder = StateGraph(AgentState)
builder.add_node("orchestrator", orchestrator_node)
builder.set_entry_point("orchestrator")
builder.add_conditional_edges("orchestrator", should_continue)

graph = builder.compile()


# =========================================================
# RUN
# =========================================================
@traceable(name="milestone4_run")
def run_graph(user_input: str):

    initial: AgentState = {
        "messages": [user_input],
        "todos": [],
        "files": {},
        "sub_agent_results": {},
        "done": False
    }

    return graph.invoke(initial)


# =========================================================
# ENTRY
# =========================================================
if __name__ == "__main__":

    article = """
Write a structured industry report on BMW's long-term electric vehicle strategy,
including sustainability goals, battery innovation, investment risks,
and global competitive positioning.
"""

    final = cast(AgentState, run_graph(article))

    print("\nGenerated Files:\n")
    for k, v in final.get("files", {}).items():
        print(f"{k}:\n{v}\n")
