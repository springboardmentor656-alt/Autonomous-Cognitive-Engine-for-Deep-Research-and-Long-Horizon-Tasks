from agent.summarization_agent import summarization_agent_app

SUB_AGENTS = {
    "summarize": summarization_agent_app
}

def task(agent_name: str, input_text: str) -> str:
    """
    Delegate a task to a specialized sub-agent.
    """

    if agent_name not in SUB_AGENTS:
        return "Unknown agent"

    result = SUB_AGENTS[agent_name].invoke({
        "input": input_text
    })

    return result["output"]
