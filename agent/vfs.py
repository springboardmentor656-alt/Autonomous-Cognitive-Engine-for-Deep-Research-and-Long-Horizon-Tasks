from langsmith import traceable

VFS = {}

@traceable(name="List Files")
def ls():
    return list(VFS.keys())

@traceable(name="Write File")
def write_file(filename: str, content: str):
    VFS[filename] = content
    return f"Written {filename}"

@traceable(name="Read File")
def read_file(filename: str):
    return VFS.get(filename, "")

@traceable(name="Edit File")
def edit_file(filename: str, new_content: str):
    VFS[filename] = new_content
    return f"Edited {filename}"
