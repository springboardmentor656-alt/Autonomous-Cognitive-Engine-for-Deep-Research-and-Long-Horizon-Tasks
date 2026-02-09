from typing import TypedDict, List, Dict

class AgentState(TypedDict):
    messages: List[dict]       # Stores user input messages
    todos: Dict[str, List[str]]  # Stores todos per task
    files: Dict[str, str]       # Virtual File System (VFS)
