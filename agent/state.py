from typing import TypedDict, List, Dict

class AgentState(TypedDict):
    messages: List[dict]
    todos: List[str]
    files: Dict[str, str]   # ✅ Virtual File System
    needs_read: bool