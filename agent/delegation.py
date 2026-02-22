from subagents.researcher import run as researcher_run
from subagents.summarizer import run as summarizer_run
from langsmith import traceable


@traceable(name="Task Delegation Tool")
def delegate_task(agent_name: str, task: str, context: str = "") -> str:

    if agent_name == "researcher":
        return researcher_run(task)

    if agent_name == "summarizer":
        return summarizer_run(task, context)

    raise ValueError(f"No sub-agent registered with name: {agent_name}")
