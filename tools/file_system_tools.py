"""
Virtual File System Tools for Context Management

These tools let the agent save, read, edit, and list files
in its working memory (state), avoiding context window limits.
"""

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Optional

class WriteFileInput(BaseModel):
    """Input for write_file tool"""
    filename: str = Field(description="Name of the file (e.g., 'analysis.txt', 'calculations.json')")
    content: str = Field(description="Content to write to the file")

class ReadFileInput(BaseModel):
    """Input for read_file tool"""
    filename: str = Field(description="Name of the file to read")

class EditFileInput(BaseModel):
    """Input for edit_file tool"""
    filename: str = Field(description="Name of the file to edit")
    content: str = Field(description="New content to replace the old content")

@tool(args_schema=WriteFileInput)
def write_file(filename: str, content: str) -> str:
    """
    Save information to a file in the virtual file system.
    
    Use this to store:
    - Calculation results
    - Research findings
    - Intermediate analysis
    - Notes for later steps
    
    Args:
        filename: Name of the file (use descriptive names like 'retirement_calc.txt')
        content: The content to save
        
    Returns:
        Confirmation message
        
    Example:
        write_file(
            filename="debt_analysis.txt",
            content="Total debt: $60,000\\nMonthly payment: $800\\nInterest rate: 18% avg"
        )
    """
    if not filename or not content:
        return "Error: Both filename and content are required"
    
    return f"Saved {len(content)} characters to '{filename}'"

@tool(args_schema=ReadFileInput)
def read_file(filename: str) -> str:
    """
    Read a file from the virtual file system.
    
    Use this to retrieve information you saved earlier.
    
    Args:
        filename: Name of the file to read
        
    Returns:
        File content or error message
        
    Example:
        read_file(filename="debt_analysis.txt")
    """
    if not filename:
        return "Error: Filename is required"
    
    return f"[This will return the content of '{filename}']"

@tool(args_schema=EditFileInput)
def edit_file(filename: str, content: str) -> str:
    """
    Update an existing file with new content.
    
    This completely replaces the file's content.
    
    Args:
        filename: Name of the file to edit
        content: New content
        
    Returns:
        Confirmation message
        
    Example:
        edit_file(
            filename="retirement_calc.txt",
            content="Updated calculation: Need $1.2M by age 65"
        )
    """
    if not filename or not content:
        return "Error: Both filename and content are required"
    
    return f"Updated '{filename}' with {len(content)} characters"

@tool
def ls() -> str:
    """
    List all files in the virtual file system.
    
    Use this to see what files you've created.
    
    Returns:
        List of filenames
        
    Example:
        ls()  # Returns: "Files: debt_analysis.txt, retirement_calc.txt"
    """
    return "[This will list all saved files]"

FILE_SYSTEM_TOOLS = [write_file, read_file, edit_file, ls]