from typing import TypedDict, Annotated, List, Dict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class TodoItem(TypedDict):
    """Individual TODO task"""
    id: int
    description: str
    status: str  
    result: str | None
    assigned_to: str | None  

class AgentState(TypedDict):
    """
    The complete state of the financial planning agent.
    This persists across all steps of execution.
    """

    messages: Annotated[List[BaseMessage], add_messages]
    

    todos: List[TodoItem]
    current_todo_id: int | None
    

    files: Dict[str, str]  
    

    user_request: str
    

    final_output: str | None
    iteration_count: int
    max_iterations: int

def create_initial_state(user_request: str, max_iterations: int = 15) -> AgentState:
    """Create initial agent state"""
    return {
        "messages": [],
        "todos": [],
        "current_todo_id": None,
        "files": {},
        "user_request": user_request,
        "final_output": None,
        "iteration_count": 0,
        "max_iterations": max_iterations
    }