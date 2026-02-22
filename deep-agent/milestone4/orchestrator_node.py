from agent.state import AgentState

def orchestrator_node(state: AgentState):

    pending = [t for t in state["todos"] if t["status"] == "pending"]

    if not pending:
        return {"next": "synthesis"}

    next_task = pending[0]

    return {
        "current_task": next_task["task"],
        "next": "execute"
    }
