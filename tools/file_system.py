def write_file(state, filename, content):
    if "files" not in state:
        state["files"] = {}

    state["files"][filename] = content
    return f"File '{filename}' written successfully."


def read_file(state, filename):
    if "files" not in state or filename not in state["files"]:
        return "File not found."

    return state["files"][filename]


def edit_file(state, filename, content):
    if "files" not in state:
        state["files"] = {}

    if filename not in state["files"]:
        return "File not found."

    state["files"][filename] += "\n" + content
    return f"File '{filename}' updated successfully."


def ls(state):
    if "files" not in state:
        return []

    return list(state["files"].keys())
