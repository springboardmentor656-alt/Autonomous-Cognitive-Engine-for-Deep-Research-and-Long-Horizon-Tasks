from langchain_core.tools import tool
from typing import List
from pydantic import BaseModel, Field

class WriteTodosInput(BaseModel):
    """Input schema for write_todos tool"""
    tasks: List[str] = Field(
        description="List of task descriptions in execution order. Each task should be a clear, actionable step."
    )

@tool(args_schema=WriteTodosInput)
def write_todos(tasks: List[str]) -> str:
    """
    Create a structured plan by breaking down a complex financial planning goal 
    into sequential sub-tasks.
    
    Use this tool when you first receive a complex financial planning request
    that requires multiple steps.
    
    Args:
        tasks: List of 3-7 task descriptions in execution order
        
    Returns:
        Confirmation message with task count
        
    Example:
        write_todos(tasks=[
            "Gather client's current financial information",
            "Calculate debt-to-income ratio",
            "Analyze investment portfolio allocation",
            "Generate retirement savings projections",
            "Create comprehensive financial plan document"
        ])
    """
    if not tasks:
        return "Error: Task list cannot be empty"
    
    if len(tasks) > 10:
        return f"Error: Too many tasks ({len(tasks)}). Please limit to 10 or fewer."
    
    task_preview = "\n".join([f"  {i+1}. {task}" for i, task in enumerate(tasks[:3])])
    if len(tasks) > 3:
        task_preview += f"\n  ... and {len(tasks) - 3} more"
    
    return f"Created {len(tasks)} tasks in the plan:\n{task_preview}"


class UpdateTodoInput(BaseModel):
    """Input schema for update_todo_status tool"""
    todo_id: int = Field(description="The ID of the task to update")
    status: str = Field(description="New status: pending, in_progress, completed, or failed")
    result: str = Field(default="", description="Optional result description if task is completed")

@tool(args_schema=UpdateTodoInput)
def update_todo_status(todo_id: int, status: str, result: str = "") -> str:
    """
    Update the status of a specific TODO task.
    
    Args:
        todo_id: The ID of the task to update
        status: New status ("pending", "in_progress", "completed", "failed")
        result: Optional result description if task is completed
        
    Returns:
        Confirmation message
    """
    valid_statuses = ["pending", "in_progress", "completed", "failed"]
    
    if status not in valid_statuses:
        return f"Error: Invalid status. Must be one of {valid_statuses}"
    
    if status == "completed" and not result:
        return "Error: Result is required when marking task as completed"
    
    return f"Task {todo_id} updated to '{status}'"

@tool
def list_todos() -> str:
    """
    List all current TODO tasks with their status.
    
    Returns:
        Formatted list of all tasks
    """
    return "Current TODO list:\n[This will show actual tasks from state]"


PLANNING_TOOLS = [write_todos, update_todo_status, list_todos]