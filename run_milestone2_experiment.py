from dotenv import load_dotenv
load_dotenv()

from langsmith.evaluation import evaluate
from agent.react_agent import app


def agent_runner(example):
    # ---- Build LangGraph state ----
    state = {
        "messages": [
            {"role": "user", "content": example["input"]}
        ],
        "todos": [],
        "files": {},
        "needs_read": False
    }

    # ---- Run agent ----
    result = app.invoke(state)

    # ---- LangSmith expects 'output' ----
    return {
        "output": result["todos"]
    }


evaluate(
    agent_runner,
    data="milestone-2-vfs-ui-comparison",          # dataset name (must exist)
    experiment_prefix="milestone-2-vfs-comparison"
)

print("✅ Experiment run complete — check LangSmith Experiments")