from langsmith import traceable
from agent_state import AgentState


@traceable(name="write_file")
def write_file(state: AgentState, filename: str, content: str) -> str:
    state["files"][filename] = content
    return filename


@traceable(name="read_file")
def read_file(state: AgentState, filename: str) -> str:
    return state["files"].get(filename, "")
