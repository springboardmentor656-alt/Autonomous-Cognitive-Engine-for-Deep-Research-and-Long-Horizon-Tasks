def orchestrator_node(state):

    index = state["current_index"]

    if index >= len(state["todos"]):
        state["next_action"] = "finalize"
        return state

    state["next_action"] = "execute"
    state["current_task"] = state["todos"][index]

    return state
