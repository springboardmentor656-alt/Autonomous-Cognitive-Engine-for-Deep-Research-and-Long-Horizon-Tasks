"""
Sub-Agent Registry

Maps specialist types to their agent implementations.
The supervisor uses this to route tasks to the right expert.
"""

from agents.sub_agents.debt_specialist import run_debt_specialist
from agents.sub_agents.budget_analyst import run_budget_analyst
from agents.sub_agents.investment_advisor import run_investment_advisor
from agents.sub_agents.tax_optimizer import run_tax_optimizer

SUB_AGENT_REGISTRY = {
    "debt_specialist": run_debt_specialist,
    "budget_analyst": run_budget_analyst,
    "investment_advisor": run_investment_advisor,
    "tax_optimizer": run_tax_optimizer
}

def delegate_to_specialist(specialist_type: str, task: str) -> str:
    """
    Delegate a task to the appropriate specialist.
    
    Args:
        specialist_type: Type of specialist (e.g., "debt_specialist")
        task: Description of what needs to be done
        
    Returns:
        The specialist's analysis and recommendations
        
    Raises:
        ValueError: If specialist type is not recognized
    """
    if specialist_type not in SUB_AGENT_REGISTRY:
        available = ", ".join(SUB_AGENT_REGISTRY.keys())
        raise ValueError(
            f"Unknown specialist: {specialist_type}. "
            f"Available specialists: {available}"
        )
    
    specialist_func = SUB_AGENT_REGISTRY[specialist_type]
    
    print(f"\n[DELEGATION] Routing to {specialist_type}...")
    print(f"[DELEGATION] Task: {task[:100]}...")
    
    try:
        result = specialist_func(task)
        print(f"[DELEGATION] {specialist_type} completed")
        return result
    except Exception as e:
        print(f"[DELEGATION] Error in {specialist_type}: {e}")
        return f"Error: {specialist_type} failed - {str(e)}"

__all__ = [
    'SUB_AGENT_REGISTRY',
    'delegate_to_specialist',
    'run_debt_specialist',
    'run_budget_analyst',
    'run_investment_advisor',
    'run_tax_optimizer'
]