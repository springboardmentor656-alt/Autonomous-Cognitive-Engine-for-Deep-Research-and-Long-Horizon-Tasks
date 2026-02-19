from typing import TypedDict, List, Dict


class AgentState(TypedDict):
    task: str
    todos: List[str]
    files: Dict[str, str]
    current_step: int
    next_action: str
    final_output: str
