from agent.sub_agents.registry import AGENT_REGISTRY

def delegate_task(agent_name: str, task: str) -> str:
    """
    Delegates a task to a registered sub-agent
    """
    if agent_name not in AGENT_REGISTRY:
        raise ValueError(f"Unknown agent: {agent_name}")

    agent_fn = AGENT_REGISTRY[agent_name]
    return agent_fn(task)
