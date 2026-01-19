from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from typing import List, Dict

from config.settings import settings
from state.agent_state import AgentState, TodoItem
from agents.prompts import get_prompt

class TaskPlanWithFiles(BaseModel):
    tasks: List[str] = Field(
        description="3-10 sequential financial planning tasks",
        min_length=3,
        max_length=10
    )
    files_to_create: Dict[str, str] = Field(
    default_factory=dict,
    description="Each file must contain detailed financial summaries, numbers, calculations, and actionable advice."
    )
    reasoning: str = Field(
        description="Brief explanation of the approach"
    )

def create_llm():
    return ChatGroq(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        groq_api_key=settings.GROQ_API_KEY
    )

def planning_node(state: AgentState) -> AgentState:
    llm = create_llm()
    structured_llm = llm.with_structured_output(TaskPlanWithFiles)

    base_prompt = get_prompt(settings.PROMPT_STYLE, milestone=2)

    prompt = f"""
{base_prompt}

User request:
{state["user_request"]}
"""

    if state["files"]:
        file_context = "\n\n".join(
            [f"{fname}:\n{content[:1200]}" for fname, content in state["files"].items()]
        )
        prompt += f"\n\nPreviously saved files:\n{file_context}"

    print("[DEBUG M2-Structured] Calling LLM with structured output...")

    try:
        response = structured_llm.invoke(prompt)

        print(f"[DEBUG M2-Structured] Tasks: {len(response.tasks)}")
        print(f"[DEBUG M2-Structured] Files: {len(response.files_to_create)}")

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
            "files": dict(response.files_to_create),
            "iteration_count": state["iteration_count"] + 1,
            "messages": [
                HumanMessage(content=f"Plan created. Reasoning: {response.reasoning}")
            ]
        }

    except Exception as e:
        print(f"[DEBUG M2-Structured] Error: {e}")
        return {
            "iteration_count": state["iteration_count"] + 1,
            "messages": [HumanMessage(content=f"Error: {str(e)}")]
        }

def create_structured_m2_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planning_node)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", END)

    return workflow.compile()

structured_agent_m2 = create_structured_m2_graph()
