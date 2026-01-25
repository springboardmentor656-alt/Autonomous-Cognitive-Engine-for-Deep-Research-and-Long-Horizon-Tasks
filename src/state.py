"""
State definition for the agent with virtual file system.
"""

from typing import TypedDict, Dict, List, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    State for the agent including conversation history and virtual file system.
    
    Attributes:
        messages: Conversation history (automatically merged)
        files: Virtual file system mapping filename to content
        intermediate_steps: Track tool usage for evaluation
    """
    messages: Annotated[List[BaseMessage], add_messages]
    files: Dict[str, str]
    intermediate_steps: List[Dict[str, str]]  # Track tool calls for evaluation