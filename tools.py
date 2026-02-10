from langchain_core.tools import tool
from sub_agent import summarization_agent

@tool
def delegate_task(agent_name: str, task_input: str) -> str:
    """
    Delegates a task to a specialized sub-agent and returns the result.
    """
    if agent_name == "summarizer":
        response = summarization_agent.invoke({"task": task_input})
        return response["result"]

    return "No suitable sub-agent found."
