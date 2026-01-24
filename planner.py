# agent/planner.py

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
import os
from langchain_core.tools import tool

from dotenv import load_dotenv

load_dotenv()

from agent.prompts import TASK_PLANNER_PROMPT


from agent.config import get_model_name, get_api_key

from agent.config import get_model_name, get_api_key, PRIMARY_PROVIDER

class TaskPlanner:
    """
    TaskPlanner uses an LLM (Groq, OpenAI, or Anthropic) to generate 
    step-by-step TODOs for a given task description.
    """

    def __init__(self, model_name: str = None, temperature: float = 0.2):
        self.model_name = model_name or get_model_name()
        self.api_key = get_api_key()
        
        # Dynamically select the LLM class based on the provider
        if PRIMARY_PROVIDER == "groq":
            from langchain_groq import ChatGroq
            self.llm = ChatGroq(model=self.model_name, temperature=temperature, api_key=self.api_key)
        elif PRIMARY_PROVIDER == "openai":
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(model=self.model_name, temperature=temperature, api_key=self.api_key)
        elif PRIMARY_PROVIDER == "anthropic":
            from langchain_anthropic import ChatAnthropic
            self.llm = ChatAnthropic(model=self.model_name, temperature=temperature, api_key=self.api_key)
        else:
            from langchain_groq import ChatGroq
            self.llm = ChatGroq(model=self.model_name, temperature=temperature, api_key=self.api_key)

    def generate_todo(self, task: str):
        """
        Generate TODO steps for a given task.
        Returns a list of numbered steps without duplicate numbering.
        """
        # Fill in the task in the prompt
        prompt = TASK_PLANNER_PROMPT.format(task=task)

        # Send the prompt to the LLM
        response = self.llm.invoke([HumanMessage(content=prompt)])

        # Extract lines starting with a number and remove duplicate numbering
        steps = []
        for line in response.content.split("\n"):
            line = line.strip()
            if line and line[0].isdigit():
                # Remove duplicate numbering (e.g., '1. 1. Research...' -> 'Research...')
                clean_line = line.split('.', 1)[1].strip()
                steps.append(clean_line)

        return steps


# -----------------------------
# Backward-compatible function
# -----------------------------
def plan_task(task: str):
    """
    Simple function to generate TODO steps using TaskPlanner.
    Useful for legacy imports.
    """
    planner = TaskPlanner()
    return planner.generate_todo(task)

# -----------------------------
# LangChain / LangGraph Tool
# -----------------------------
from langchain_core.tools import tool

@tool
def write_todos(task: str) -> list:
    """
    LangGraph / LangChain tool to generate a structured TODO list
    from a high-level task description.
    """
    planner = TaskPlanner()
    todos = planner.generate_todo(task)
    return todos

# -----------------------------
# Simple example usage
# -----------------------------
if __name__ == "__main__":
    task = "Build a personal website with a home page, about page, and contact form"

    planner = TaskPlanner(
        model_name="llama-3.3-70b-versatile",
        temperature=0.2
    )

    todos = planner.generate_todo(task)

    print("Generated TODO steps:")
    for i, step in enumerate(todos, start=1):
        print(f"{i}. {step}")
