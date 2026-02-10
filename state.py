from typing import TypedDict, List, Dict

class AgentState(TypedDict):
    user_input: str
    todos: List[str]
    delegated_results: Dict[str, str]
