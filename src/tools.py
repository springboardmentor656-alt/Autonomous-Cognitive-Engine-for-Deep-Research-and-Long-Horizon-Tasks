"""
Virtual file system tools for context offloading.
These tools allow the agent to save and retrieve information.
"""

from langchain_core.tools import tool
from typing import Dict

# Global reference to current state (set by graph during execution)
_current_state = {"state": None}


@tool
def ls() -> str:
    """
    List all files in the virtual file system.
    Use this to see what files have been created.
    
    Returns:
        String listing all filenames, or message if no files exist.
    """
    state = _current_state["state"]
    if not state or 'files' not in state:
        return "📁 File system not initialized."
    
    files = state['files']
    if not files:
        return "📁 No files in the file system. Use write_file to create files."
    
    file_list = "\n".join([f"  • {filename} ({len(content)} chars)" 
                           for filename, content in files.items()])
    return f"📁 Files in system ({len(files)} total):\n{file_list}"


@tool
def read_file(filename: str) -> str:
    """
    Read the content of a file from the virtual file system.
    Use this to retrieve information you previously saved.
    
    Args:
        filename: The name of the file to read (e.g., 'summary1.txt')
        
    Returns:
        The content of the file, or an error message if not found.
    """
    state = _current_state["state"]
    if not state or 'files' not in state:
        return f"❌ Error: File system not initialized."
    
    files = state['files']
    if filename not in files:
        available = ", ".join(files.keys()) if files else "none"
        return f"❌ Error: File '{filename}' not found. Available files: {available}"
    
    content = files[filename]
    return f"📄 Content of '{filename}':\n{content}"


@tool
def write_file(filename: str, content: str) -> str:
    """
    Write content to a file in the virtual file system.
    Creates a new file or overwrites existing file.
    USE THIS to save intermediate results, summaries, or any information you need later.
    
    Args:
        filename: The name of the file (e.g., 'summary_article1.txt')
        content: The content to write to the file
        
    Returns:
        Confirmation message with file details.
    """
    state = _current_state["state"]
    if not state or 'files' not in state:
        return f"❌ Error: File system not initialized."
    
    # Save the file
    state['files'][filename] = content
    
    # Track this action for evaluation
    if 'intermediate_steps' in state:
        state['intermediate_steps'].append({
            'tool': 'write_file',
            'filename': filename,
            'size': len(content)
        })
    
    return f"✅ Successfully wrote {len(content)} characters to '{filename}'"


@tool
def edit_file(filename: str, new_content: str) -> str:
    """
    Edit an existing file by replacing its content.
    File must already exist (use write_file to create new files).
    
    Args:
        filename: The name of the file to edit
        new_content: The new content to replace the old content
        
    Returns:
        Confirmation message or error if file doesn't exist.
    """
    state = _current_state["state"]
    if not state or 'files' not in state:
        return f"❌ Error: File system not initialized."
    
    files = state['files']
    if filename not in files:
        available = ", ".join(files.keys()) if files else "none"
        return f"❌ Error: File '{filename}' not found. Available files: {available}. Use write_file to create it."
    
    # Update the file
    old_size = len(files[filename])
    files[filename] = new_content
    new_size = len(new_content)
    
    # Track this action
    if 'intermediate_steps' in state:
        state['intermediate_steps'].append({
            'tool': 'edit_file',
            'filename': filename,
            'old_size': old_size,
            'new_size': new_size
        })
    
    return f"✅ Successfully edited '{filename}' (was {old_size} chars, now {new_size} chars)"


# Export all tools
file_system_tools = [ls, read_file, write_file, edit_file]
all_tools = file_system_tools