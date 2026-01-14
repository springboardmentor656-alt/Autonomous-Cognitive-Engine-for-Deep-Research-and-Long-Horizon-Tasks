"""
Alternative agent using structured outputs instead of tool calling.
This works better with some Groq models that struggle with tool use.
"""

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from typing import List

from config.settings import settings
from state.agent_state import AgentState, TodoItem

class TaskPlan(BaseModel):
    """Structured output for task planning"""
    tasks: List[str] = Field(
        description="List of 3-7 sequential tasks needed to complete the request",
        min_length=3,
        max_length=10
    )
    reasoning: str = Field(
        description="Brief explanation of the task breakdown approach"
    )

STRUCTURED_PROMPT = """You are a financial planning expert. Break down the user's request into 3-7 sequential tasks.

User request: {request}

Provide a structured task plan with:
- tasks: List of specific, actionable steps
- reasoning: Brief explanation of your approach

Be specific and use financial planning best practices."""

def planning_node(state: AgentState) -> AgentState:
    """Use structured output to generate task plan"""
    
    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        groq_api_key=settings.GROQ_API_KEY
    )
    
    structured_llm = llm.with_structured_output(TaskPlan)
    
    prompt = STRUCTURED_PROMPT.format(request=state["user_request"])
    
    print(f"[DEBUG] Calling LLM with structured output...")
    
    try:
        response = structured_llm.invoke(prompt)
        
        print(f"[DEBUG] Got {len(response.tasks)} tasks")
        
        todos = [
            TodoItem(
                id=i,
                description=task,
                status="pending",
                result=None,
                assigned_to="main"
            )
            for i, task in enumerate(response.tasks)
        ]
        
        return {
            "todos": todos,
            "iteration_count": state["iteration_count"] + 1,
            "messages": [HumanMessage(content=f"Created plan: {response.reasoning}")]
        }
        
    except Exception as e:
        print(f"[DEBUG] Error: {e}")
        return {
            "iteration_count": state["iteration_count"] + 1,
            "messages": [HumanMessage(content=f"Error: {str(e)}")]
        }

def create_structured_output_graph():
    """
    Create a simple graph using structured outputs instead of tools.
    This is more reliable with Groq models.
    """
    workflow = StateGraph(AgentState)
    
    workflow.add_node("planner", planning_node)
    
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", END)
    
    return workflow.compile()

structured_agent = create_structured_output_graph()