from agent.delegation_tool import task
from agent.vfs_tools import write_file


def execute_node(state):

    # Safety check
    if not state.get("todos"):
        state["completed"] = True
        return state

    next_task = state["todos"].pop(0)
    state["current_task"] = next_task

    result = task(
        agent_name="summarize",
        input_text=next_task
    )

    filename = f"{next_task[:20]}.txt"

    write_file(
        filename=filename,
        content=result,
        state=state
    )

    # If after popping, todos empty → mark completed
    if not state["todos"]:
        state["completed"] = True

    return state
