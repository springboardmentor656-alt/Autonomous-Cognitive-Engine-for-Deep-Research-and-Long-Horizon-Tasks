from langchain_core.tools import tool
from agent.summarization_agent import summarization_agent_app

SUB_AGENTS = {
    "summarize": summarization_agent_app
}

@tool
def task(agent_name: str, input_text: str) -> str:
    """
    Delegate a task to a specialized sub-agent.
    """
    if agent_name not in SUB_AGENTS:
        return f"Unknown agent: {agent_name}"

    sub_agent = SUB_AGENTS[agent_name]

    result = sub_agent.invoke({
        "input": input_text
    })

    return result["output"]