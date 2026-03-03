from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    """
    TASK 1: Consolidated State for the Grand Integration.
    Includes fields for Planning, File System, and Delegation.
    """
    messages: Annotated[List[str], operator.add]
    todos: List[dict]           # Milestone 1: Planning
    files: dict                 # Milestone 2: Virtual File System
    sub_agent_results: List[str] # Milestone 3: Delegation
    dataset_item: str
    current_task: str