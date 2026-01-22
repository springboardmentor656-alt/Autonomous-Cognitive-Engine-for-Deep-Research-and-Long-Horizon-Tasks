"""
Delegation Tools for Multi-Agent Collaboration

The supervisor agent uses these tools to delegate tasks to specialized sub-agents.
"""

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Literal

class DelegateTaskInput(BaseModel):
    """Input schema for delegate_task tool"""
    task_description: str = Field(
        description="Clear description of the task to delegate"
    )
    specialist: Literal["debt_specialist", "budget_analyst", "investment_advisor", "tax_optimizer"] = Field(
        description="Which specialist to delegate to"
    )

@tool(args_schema=DelegateTaskInput)
def delegate_task(task_description: str, specialist: str) -> str:
    """
    Delegate a specialized task to a sub-agent expert.
    
    Use this when you need expert help with:
    - Debt analysis/payoff strategies → "debt_specialist"
    - Budget creation/expense analysis → "budget_analyst"
    - Investment/retirement planning → "investment_advisor"
    - Tax optimization strategies → "tax_optimizer"
    
    The specialist will analyze the task and return detailed results.
    
    Args:
        task_description: Clear description of what you need done
        specialist: Which expert to delegate to
        
    Returns:
        The specialist's analysis and recommendations
        
    Example:
        delegate_task(
            task_description="Calculate optimal debt payoff strategy for $60k in credit card debt",
            specialist="debt_specialist"
        )
    """
    return f"[Delegating to {specialist}: {task_description}]"

DELEGATION_TOOLS = [delegate_task]