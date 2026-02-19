from dotenv import load_dotenv
load_dotenv()

from langsmith import Client

client = Client()

DATASET_NAME = "autonomous_research_eval"

tasks = [
    "Generate a research report on Quantum Computing applications",
    "Generate a research report on Artificial Intelligence in healthcare",
    "Generate a research report on Blockchain use cases in finance",
    "Generate a research report on Renewable Energy technologies",
    "Generate a research report on Cybersecurity threats and solutions"
]

for task in tasks:
    client.create_example(
        inputs={"task": task},
        outputs={},  # No fixed expected output (LLM-as-judge later)
        dataset_name=DATASET_NAME
    )

print("Examples added to dataset")
