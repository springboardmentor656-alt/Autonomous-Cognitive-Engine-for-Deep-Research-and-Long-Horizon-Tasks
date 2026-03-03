import os
from typing import Dict
# Change from 'from state' to:
from graph.state import AgentState

def write_file(state: AgentState, filename: str, content: str) -> str:
    
    """
    Milestone 2: Context Offloading.
    Saves information to the agent's internal virtual file system.
    """
    if "files" not in state:
        state["files"] = {}
    
    state["files"][filename] = content
    print(f"      [VIRTUAL FS] 💾 Written: {filename} ({len(content)} characters)")
    return f"Successfully saved to {filename}."

def read_file(state: AgentState, filename: str) -> str:
    """
    Milestone 2: Context Retrieval.
    Retrieves information from the agent's internal virtual file system.
    """
    content = state.get("files", {}).get(filename)
    
    if content:
        print(f"      [VIRTUAL FS] 📖 Read: {filename}")
        return content
    else:
        return f"Error: The file '{filename}' does not exist in the virtual system."

def list_files(state: AgentState) -> str:
    """Provides a list of all files currently stored in memory."""
    files = list(state.get("files", {}).keys())
    if not files:
        return "The virtual file system is empty."
    return "Stored files: " + ", ".join(files)