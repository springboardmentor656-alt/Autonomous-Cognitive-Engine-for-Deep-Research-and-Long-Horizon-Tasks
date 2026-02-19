import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv()

from langsmith.evaluation import evaluate
from agent.graph import build_graph

DATASET_NAME = "milestone4_research_tasks"
EXPERIMENT_PREFIX = "milestone4_full_agent"

app = build_graph()

def agent_runner(inputs: dict):
    result = app.invoke({
        "task": inputs["task"],
        "todos": [],
        "files": {},
        "final_output": ""
    })

    final_output = result.get("final_output")

    if not final_output:
        final_output = "ERROR: final_output was not produced by the agent"

    return {
        "output": final_output
    }



evaluate(
    agent_runner,
    data="milestone4_research_tasks",
    experiment_prefix="milestone4_full_agent",
)