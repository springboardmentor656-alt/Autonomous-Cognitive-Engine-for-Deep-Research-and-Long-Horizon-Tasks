"""
Tax Optimizer Sub-Agent

Expert in:
- Tax-saving strategies
- Deductions & credits
- Income tax planning
- Capital gains optimization
"""

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import TypedDict
from pydantic import BaseModel, Field

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings


class TaxOptimizerState(TypedDict):
    task: str
    analysis: str
    recommendation: str
    completed: bool


TAX_OPTIMIZER_PROMPT = """You are a Tax Optimization Expert with knowledge of:

- Income tax strategies
- Legal deductions & credits
- Retirement tax benefits
- Capital gains planning
- Tax-efficient investing

Your job: Reduce tax burden legally and smartly.

ALWAYS structure your response as:

ANALYSIS:
[Tax situation analysis]

RECOMMENDATION:
[Specific tax-saving steps]

CALCULATIONS:
[Estimated tax savings]
"""


class TaxPlan(BaseModel):
    analysis: str = Field(description="Tax situation analysis")
    recommendation: str = Field(description="Tax-saving strategies")
    calculations: str = Field(description="Estimated savings")


def tax_analysis_node(state: TaxOptimizerState) -> TaxOptimizerState:
    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=0.1,
        groq_api_key=settings.GROQ_API_KEY
    )

    structured_llm = llm.with_structured_output(TaxPlan)

    prompt = f"""{TAX_OPTIMIZER_PROMPT}

TASK:
{state['task']}

Provide a detailed tax optimization plan.
"""

    try:
        response = structured_llm.invoke(prompt)

        full_report = f"""
TAX OPTIMIZATION REPORT
======================

{response.analysis}

RECOMMENDATION
==============

{response.recommendation}

CALCULATIONS
============

{response.calculations}
"""

        return {
            "analysis": full_report,
            "recommendation": response.recommendation,
            "completed": True
        }

    except Exception as e:
        return {
            "analysis": f"Error creating tax plan: {str(e)}",
            "recommendation": "Unable to provide tax advice.",
            "completed": True
        }


def create_tax_optimizer():
    workflow = StateGraph(TaxOptimizerState)
    workflow.add_node("analyze", tax_analysis_node)
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", END)
    return workflow.compile()


tax_optimizer_agent = create_tax_optimizer()


def run_tax_optimizer(task: str) -> str:
    initial_state = {
        "task": task,
        "analysis": "",
        "recommendation": "",
        "completed": False
    }

    result = tax_optimizer_agent.invoke(initial_state)
    return result["analysis"]
