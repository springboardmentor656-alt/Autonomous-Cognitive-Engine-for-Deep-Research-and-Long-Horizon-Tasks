from subagents.summarizer import run as summarizer_run
from langsmith import traceable

@traceable(name="Task Delegation Tool")
def delegate_task(agent_name: str, task: str) -> str:
    if agent_name == "summarizer":
        return summarizer_run(task)

    raise ValueError(f"No sub-agent registered with name: {agent_name}")
