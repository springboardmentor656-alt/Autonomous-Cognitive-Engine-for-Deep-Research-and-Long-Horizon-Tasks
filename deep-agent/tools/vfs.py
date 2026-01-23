from langchain_core.tools import tool

@tool
def write_file(filename: str, content: str, state: dict) -> str:
    """
    Write content to virtual file system (stored in state).
    """
    state["files"][filename] = content
    return f"Saved content to {filename}"

@tool
def read_file(filename: str, state: dict) -> str:
    """
    Read content from virtual file system.
    """
    return state["files"].get(filename, "")

@tool
def ls(state: dict) -> list:
    """
    List files in virtual file system.
    """
    return list(state["files"].keys())

@tool
def edit_file(filename: str, content: str, state: dict) -> str:
    """
    Edit an existing virtual file.
    """
    state["files"][filename] = content
    return f"Updated {filename}"