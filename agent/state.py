from typing import TypedDict

class AgentState(TypedDict):
    task: str
    todos: list
    files: dict
    final_output: str
