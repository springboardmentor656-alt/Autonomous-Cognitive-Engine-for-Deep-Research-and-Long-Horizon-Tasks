from agent.sub_agents.registry import SUB_AGENT_REGISTRY

def delegate_task(agent_name: str, task: str) -> str:
    """
    Delegates a task to a specialized sub-agent
    """
    if agent_name not in SUB_AGENT_REGISTRY:
        raise ValueError(f"No sub-agent found for: {agent_name}")

    sub_agent = SUB_AGENT_REGISTRY[agent_name]
    return sub_agent(task)
