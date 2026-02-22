from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    task: str
    todos: List[str]
    current_index: int
    delegated_results: List[str]
    current_todo: Optional[str]
    next_step: Optional[str]
    final_output: str
    evaluation: str
    execution_time: float
