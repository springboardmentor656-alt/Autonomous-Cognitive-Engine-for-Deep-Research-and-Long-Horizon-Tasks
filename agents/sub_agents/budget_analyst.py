"""
Budget Analyst Sub-Agent

Expert in budget creation, expense analysis, and cash flow optimization.
"""

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from typing import TypedDict
from pydantic import BaseModel, Field

import sys
import os
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings

class BudgetAnalystState(TypedDict):
    """State for budget analyst agent"""
    task: str
    analysis: str
    budget_plan: str
    completed: bool

BUDGET_ANALYST_PROMPT = """You are a Budget Analysis Specialist with expertise in:
- Income and expense tracking
- Budget categorization (50/30/20 rule, zero-based budgeting)
- Cash flow optimization
- Savings rate analysis
- Expense reduction strategies

Your job: Analyze financial situations and create actionable budgets.

ALWAYS structure your response as:

ANALYSIS:
[Income/expense breakdown and insights]

BUDGET PLAN:
[Detailed budget with categories and amounts]

SAVINGS OPPORTUNITIES:
[Specific ways to reduce expenses or increase savings]

Use percentages and actual dollar amounts."""

class BudgetAnalysis(BaseModel):
    """Structured output for budget analysis"""
    analysis: str = Field(description="Income and expense analysis")
    budget_plan: str = Field(description="Detailed budget breakdown")
    savings_opportunities: str = Field(description="Recommendations for savings")

def budget_analysis_node(state: BudgetAnalystState) -> BudgetAnalystState:
    """Main analysis node for budget analyst"""
    
    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=0.1,
        groq_api_key=settings.GROQ_API_KEY
    )
    
    structured_llm = llm.with_structured_output(BudgetAnalysis)
    
    prompt = f"""{BUDGET_ANALYST_PROMPT}

TASK:
{state['task']}

Provide detailed budget analysis and plan."""
    
    try:
        response = structured_llm.invoke(prompt)
        
        full_analysis = f"""
BUDGET ANALYST REPORT
====================

{response.analysis}

BUDGET PLAN
===========

{response.budget_plan}

SAVINGS OPPORTUNITIES
====================

{response.savings_opportunities}
"""
        
        return {
            "analysis": full_analysis,
            "budget_plan": response.budget_plan,
            "completed": True
        }
        
    except Exception as e:
        print(f"[Budget Analyst Error] {e}")
        return {
            "analysis": f"Error analyzing budget: {str(e)}",
            "budget_plan": "Unable to create budget due to error",
            "completed": True
        }

def create_budget_analyst():
    """Create the budget analyst agent graph"""
    workflow = StateGraph(BudgetAnalystState)
    
    workflow.add_node("analyze", budget_analysis_node)
    
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", END)
    
    return workflow.compile()

budget_analyst_agent = create_budget_analyst()

def run_budget_analyst(task: str) -> str:
    """
    Run the budget analyst on a task.
    
    Args:
        task: Description of the budget analysis needed
        
    Returns:
        Detailed budget analysis and plan
    """
    initial_state = {
        "task": task,
        "analysis": "",
        "budget_plan": "",
        "completed": False
    }
    
    result = budget_analyst_agent.invoke(initial_state)
    return result["analysis"]