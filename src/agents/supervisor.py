import os
from langsmith import traceable
from graph.state import AgentState

@traceable(name="Strategic_Planner")
def supervisor_planner(state: AgentState):
    """TASK 1: The Planning Node (Creates the TODO list)"""
    topic = state.get("dataset_item") or "General Research"
    print(f"\n[PLANNER] 🧠 Creating Strategic Plan for: {topic}")
    
    # Logic to create the TODO list for Milestone 1
    state["todos"] = [
        {"task": f"Research key trends in {topic}", "status": "pending"},
        {"task": f"Summarize technical benefits of {topic}", "status": "pending"},
        {"task": "Finalize structured report", "status": "pending"}
    ]
    return state

@traceable(name="Master_Orchestrator")
def orchestrator(state: AgentState):
    """
    TASK 2: The Orchestrator Node (Conditional Logic).
    Decides based on the current TODO task what to do next.
    """
    todos = state.get("todos", [])
    pending = [t for t in todos if t["status"] == "pending"]

    if not pending:
        return "finalize"

    current_task = pending[0]["task"]
    print(f"[ORCHESTRATOR] 🧭 Deciding next step for: {current_task}")
    
    # Operational Rules for Autonomy
    if any(word in current_task for word in ["Research", "Find", "Search"]):
        return "research_node"
    elif "Summarize" in current_task:
        return "sub_agent_node"
    else:
        return "process_node"