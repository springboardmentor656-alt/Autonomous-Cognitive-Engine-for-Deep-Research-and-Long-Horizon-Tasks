def ls(state):
    """List virtual files in state."""
    return list(state["files"].keys())


def write_file(state, filename: str, content: str):
    """Create or overwrite a virtual file."""
    state["files"][filename] = content
    return f"File '{filename}' written successfully."


def read_file(state, filename: str):
    """Read a virtual file by name."""
    if filename not in state["files"]:
        return "File not found."
    return state["files"][filename]


def edit_file(state, filename: str, new_content: str):
    """Update an existing virtual file."""
    if filename not in state["files"]:
        return "File not found."
    state["files"][filename] = new_content
    return f"File '{filename}' updated successfully."
