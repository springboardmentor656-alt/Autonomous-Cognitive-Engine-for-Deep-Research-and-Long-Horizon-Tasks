"""
Virtual File System (VFS)
Stores all files inside LangGraph state["files"].
No disk writes. Fully in-memory.
"""


def write_file(filename: str, content: str, state: dict) -> str:
    """
    Write content to the virtual file system.
    Creates file if it doesn't exist.
    Overwrites if it does.
    """
    if "files" not in state:
        state["files"] = {}

    state["files"][filename] = content
    return f"Saved content to '{filename}'"


def read_file(filename: str, state: dict) -> str:
    """
    Read content from virtual file system.
    Returns empty string if file does not exist.
    """
    if "files" not in state:
        return ""

    return state["files"].get(filename, "")


def ls(state: dict) -> list:
    """
    List all files in virtual file system.
    """
    if "files" not in state:
        return []

    return list(state["files"].keys())


def edit_file(filename: str, new_content: str, state: dict) -> str:
    """
    Edit an existing file in virtual file system.
    If file doesn't exist, creates it.
    """
    if "files" not in state:
        state["files"] = {}

    state["files"][filename] = new_content
    return f"Updated '{filename}'"


def delete_file(filename: str, state: dict) -> str:
    """
    Delete file from virtual file system.
    """
    if "files" not in state:
        return "No files exist."

    if filename in state["files"]:
        del state["files"][filename]
        return f"Deleted '{filename}'"

    return f"File '{filename}' not found."
