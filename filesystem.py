from typing import Annotated, Optional
from langchain_core.tools import tool, StructuredTool
from langgraph.prebuilt import InjectedState

# -------------------------------------------------
# Core Logic Functions (Directly Callable)
# -------------------------------------------------

def list_files(state: dict = None) -> str:
    """Core logic to list files."""
    if state is None:
        return "Error: No state provided"
    
    files = state.get("files", {})
    return str(list(files.keys()))

def read_file_content(filename: str, state: dict = None) -> str:
    """Core logic to read a file."""
    if state is None:
        return "Error: No state provided"
        
    files = state.get("files", {})
    if filename not in files:
        return f"Error: {filename} not found."
    return files[filename]

def write_file_content(filename: str, content: str, state: dict = None) -> str:
    """Core logic to write to a file."""
    if state is None:
        return "Error: No state provided"
        
    if "files" not in state:
        state["files"] = {}
        
    state["files"][filename] = content
    return f"Successfully wrote to {filename}"

def edit_file_content(filename: str, old_text: str, new_text: str, state: dict = None) -> str:
    """Core logic to edit a file."""
    if state is None:
        return "Error: No state provided"
        
    files = state.get("files", {})
    if filename not in files:
        return f"Error: {filename} not found."
    
    content = files[filename]
    if old_text not in content:
        return f"Error: '{old_text}' not found in {filename}"
        
    new_content = content.replace(old_text, new_text)
    files[filename] = new_content
    return f"Successfully edited {filename}"


# -------------------------------------------------
# LangChain / LangGraph Tools
# -------------------------------------------------

@tool
def ls(path: str = ".", state: Annotated[dict, InjectedState] = None) -> str:
    """List files in the virtual file system."""
    return list_files(state)

@tool
def read_file(filename: str, state: Annotated[dict, InjectedState] = None) -> str:
    """Read the contents of a file from the virtual file system."""
    return read_file_content(filename, state)

@tool
def write_file(filename: str, content: str, state: Annotated[dict, InjectedState] = None) -> str:
    """Write content to a file in the virtual file system."""
    return write_file_content(filename, content, state)

@tool
def edit_file(filename: str, old_text: str, new_text: str, state: Annotated[dict, InjectedState] = None) -> str:
    """Edit a file in the virtual file system."""
    return edit_file_content(filename, old_text, new_text, state)
