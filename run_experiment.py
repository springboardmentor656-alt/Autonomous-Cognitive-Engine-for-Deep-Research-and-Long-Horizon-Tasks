from dotenv import load_dotenv
load_dotenv()

from langsmith import Client
from langsmith.evaluation import evaluate
from agent.react_agent import app

client = Client()

dataset = client.read_dataset(
    dataset_name="milestone-1-todo-eval"
)

def agent_runner(example):
    prompt = example["input"]

    state = {
        "messages": [{"role": "user", "content": prompt}],
        "todos": []
    }

    result = app.invoke(state)

    return {"output": result["todos"]}

evaluate(agent_runner, data=dataset)

print("Evaluation complete — check LangSmith")
