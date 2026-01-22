"""
Investment Advisor Sub-Agent

Expert in:
- Retirement planning
- Portfolio allocation
- Risk management
- Investment strategies
- Long-term wealth building
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


class InvestmentAdvisorState(TypedDict):
    task: str
    analysis: str
    recommendation: str
    completed: bool


INVESTMENT_ADVISOR_PROMPT = """You are an Investment Advisor with expertise in:

- Retirement planning
- Portfolio diversification
- Risk tolerance assessment
- Asset allocation
- Long-term investment strategies

Your job: Create smart, realistic investment plans.

ALWAYS structure your response as:

ANALYSIS:
[Your detailed investment analysis]

RECOMMENDATION:
[Clear, actionable investment plan]

CALCULATIONS:
[Projections, growth estimates, assumptions]
"""


class InvestmentPlan(BaseModel):
    analysis: str = Field(description="Detailed investment analysis")
    recommendation: str = Field(description="Specific investment strategy")
    calculations: str = Field(description="Projected returns and assumptions")


def investment_analysis_node(state: InvestmentAdvisorState) -> InvestmentAdvisorState:
    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=0.1,
        groq_api_key=settings.GROQ_API_KEY
    )

    structured_llm = llm.with_structured_output(InvestmentPlan)

    prompt = f"""{INVESTMENT_ADVISOR_PROMPT}

TASK:
{state['task']}

Provide a detailed investment plan.
"""

    try:
        response = structured_llm.invoke(prompt)

        full_report = f"""
INVESTMENT ADVISOR REPORT
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
            "analysis": full_report,
            "recommendation": response.recommendation,
            "completed": True
        }

    except Exception as e:
        return {
            "analysis": f"Error creating investment plan: {str(e)}",
            "recommendation": "Unable to provide investment advice.",
            "completed": True
        }


def create_investment_advisor():
    workflow = StateGraph(InvestmentAdvisorState)
    workflow.add_node("analyze", investment_analysis_node)
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", END)
    return workflow.compile()


investment_advisor_agent = create_investment_advisor()


def run_investment_advisor(task: str) -> str:
    initial_state = {
        "task": task,
        "analysis": "",
        "recommendation": "",
        "completed": False
    }

    result = investment_advisor_agent.invoke(initial_state)
    return result["analysis"]
