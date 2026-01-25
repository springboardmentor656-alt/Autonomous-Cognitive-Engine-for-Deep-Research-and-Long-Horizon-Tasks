from dotenv import load_dotenv
load_dotenv()

from langsmith.evaluation import evaluate
from agent.react_agent import app

DATASET_NAME = "todo-playground-dataset"


def agent_runner(example):
    """
    Called by LangSmith for each dataset row.
    """

    state = {
        "messages": [
            {"role": "user", "content": example["task"]}
        ],
        "todos": []
    }

    # Run your agent
    result = app.invoke(state)

    # Convert structured todos → text output for LangSmith
    todos_text = "\n".join(
        [todo["task"] for todo in result.get("todos", [])]
    )

    return {
        "output": todos_text
    }


# Run evaluation
evaluate(
    agent_runner,
    data=DATASET_NAME
)

print("✅ Experiment created. Check LangSmith → Datasets & Experiments.")
