from typing import TypedDict, List, Dict

class AgentState(TypedDict):
    messages: List[dict]
    todos: List[str]
    files: Dict[str, str]
    current_task: str
    completed: bool
