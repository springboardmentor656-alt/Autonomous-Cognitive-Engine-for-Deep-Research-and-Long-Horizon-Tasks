from dotenv import load_dotenv
load_dotenv()

import os
from langsmith import Client
from agent import app

# LangSmith client
client = Client()

PROJECT = os.getenv("LANGSMITH_PROJECT")
DATASET_NAME = "milestone-2-context-offloading-dataset"  # must exist in LangSmith


def run_experiment():
    examples = list(client.list_examples(dataset_name=DATASET_NAME))

    print(f"\n🧪 Running experiment on dataset: {DATASET_NAME}")
    print(f"📦 Total inputs: {len(examples)}\n")

    for ex in examples:
        prompt = list(ex.inputs.values())[0]

        state = {
            "messages": [prompt],
            "todos": [],
            "files": {}
        }

        # Run agent (traced automatically)
        app.invoke(state)

        # Print trace link (project-level, latest run on top)
        print("✅ Experiment input executed")
        print("🔗 Trace link:")
        print(f"https://smith.langchain.com/projects/{PROJECT}/runs\n")


if __name__ == "__main__":
    run_experiment()
