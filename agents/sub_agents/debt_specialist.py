"""
Debt Specialist Sub-Agent

Expert in debt analysis and payoff strategies.
Knows about: avalanche method, snowball method, consolidation, debt-to-income ratios.
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

class DebtSpecialistState(TypedDict):
    """State for debt specialist agent"""
    task: str
    analysis: str
    recommendation: str
    completed: bool

DEBT_SPECIALIST_PROMPT = """You are a Debt Management Specialist with expertise in:
- Debt payoff strategies (avalanche, snowball, consolidation)
- Interest rate optimization
- Debt-to-income ratio analysis
- Payment scheduling
- Credit score impact

Your job: Analyze debt situations and provide actionable strategies.

ALWAYS structure your response as:

ANALYSIS:
[Your detailed analysis]

RECOMMENDATION:
[Specific, actionable steps]

CALCULATIONS:
[Show your math if doing calculations]

Be specific with numbers, timelines, and exact steps."""

class DebtAnalysis(BaseModel):
    """Structured output for debt analysis"""
    analysis: str = Field(description="Detailed debt situation analysis")
    recommendation: str = Field(description="Specific payoff strategy and steps")
    calculations: str = Field(description="Supporting calculations and math")

def debt_analysis_node(state: DebtSpecialistState) -> DebtSpecialistState:
    """Main analysis node for debt specialist"""
    
    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=0.1, 
        groq_api_key=settings.GROQ_API_KEY
    )
    
    structured_llm = llm.with_structured_output(DebtAnalysis)
    
    prompt = f"""{DEBT_SPECIALIST_PROMPT}

TASK:
{state['task']}

Provide detailed debt analysis and recommendations."""
    
    try:
        response = structured_llm.invoke(prompt)
        
        full_analysis = f"""
DEBT SPECIALIST ANALYSIS
========================

{response.analysis}

RECOMMENDATION
==============

{response.recommendation}

CALCULATIONS
============

{response.calculations}
"""
        
        return {
            "analysis": full_analysis,
            "recommendation": response.recommendation,
            "completed": True
        }
        
    except Exception as e:
        print(f"[Debt Specialist Error] {e}")
        return {
            "analysis": f"Error analyzing debt: {str(e)}",
            "recommendation": "Unable to provide recommendation due to error",
            "completed": True
        }

def create_debt_specialist():
    """Create the debt specialist agent graph"""
    workflow = StateGraph(DebtSpecialistState)
    
    workflow.add_node("analyze", debt_analysis_node)
    
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", END)
    
    return workflow.compile()

debt_specialist_agent = create_debt_specialist()

def run_debt_specialist(task: str) -> str:
    """
    Run the debt specialist on a task.
    
    Args:
        task: Description of the debt analysis needed
        
    Returns:
        Detailed analysis and recommendations
    """
    initial_state = {
        "task": task,
        "analysis": "",
        "recommendation": "",
        "completed": False
    }
    
    result = debt_specialist_agent.invoke(initial_state)
    return result["analysis"]