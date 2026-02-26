from dotenv import load_dotenv
load_dotenv()

from main import graph
from langsmith import traceable

@traceable(name="delegate_task")
def delegate_task(state: AgentState, subagent_name: str, task_payload: Dict[str, Any]) -> Dict[str, Any]:

    sub_state: AgentState = {
        "messages": [task_payload.get("text", "")],
        "todos": [],
        "files": state["files"],   # 🔥 CRITICAL FIX
        "done": False
    }

    if subagent_name == "Summarization_Agent":
        final_sub_state = summarization_graph.invoke(sub_state)

    return {
        "files": final_sub_state.get("files", {}),
        "messages": final_sub_state.get("messages", []),
        "done": final_sub_state.get("done", False)
    }
