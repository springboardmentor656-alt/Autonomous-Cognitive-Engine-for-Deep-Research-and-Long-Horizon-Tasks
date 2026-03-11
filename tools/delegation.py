from langsmith import traceable
from agent.subagents.summarizer import summarization_agent
from agent.subagents.researcher import research_agent
from agent.subagents.web_search import web_search_agent

SUBAGENT_REGISTRY = {
    "summarization_agent": {
        "callable": summarization_agent,
        "description": "Summarizes provided text into a concise summary.",
        "input_key": "text",
    },
    "researcher_agent": {
        "callable": research_agent,
        "description": "Drafts a concise research response from a question.",
        "input_key": "question",
    },
    "web_search_agent": {
        "callable": web_search_agent,
        "description": "Fetches lightweight web search findings for a query.",
        "input_key": "query",
    },
}


def list_subagents():
    """Return sub-agent metadata used for routing."""
    return {
        name: {
            "description": meta["description"],
            "input_key": meta["input_key"],
        }
        for name, meta in SUBAGENT_REGISTRY.items()
    }


@traceable(name="delegate_task_tool")
def delegate_task(task_input: str, agent_name: str) -> str:
    """Route a task to a registered sub-agent."""
    if agent_name not in SUBAGENT_REGISTRY:
        return f"Sub-agent '{agent_name}' not found."

    agent_fn = SUBAGENT_REGISTRY[agent_name]["callable"]
    return agent_fn(task_input)
