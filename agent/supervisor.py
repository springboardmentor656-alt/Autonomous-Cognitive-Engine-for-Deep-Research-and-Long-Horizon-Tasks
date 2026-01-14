from langsmith import traceable
from tools.planning import write_todos

@traceable(name="supervisor_agent")
def supervisor_agent(user_input: str):
    
    state = {
        "input": user_input,
        "todos": [],
        "status": "planning"
    }

    # REASON
    print("Agent reasoning: planning required.")

    # ACT
    todos = write_todos(user_input)

    # OBSERVE
    state["todos"] = todos
    state["status"] = "planned"

    return state
