from typing import TypedDict, List, Dict, Any, Literal


class Todo(TypedDict):
    id: int
    description: str
    status: Literal["pending", "completed"]


class AgentState(TypedDict):
    messages: List[str]
    todos: List[Todo]
    files: Dict[str, str]
    sub_agent_results: Dict[str, Any]
    done: bool
