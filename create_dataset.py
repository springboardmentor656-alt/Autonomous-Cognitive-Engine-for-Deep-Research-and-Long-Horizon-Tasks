from dotenv import load_dotenv
load_dotenv()
from langsmith import Client
import json

client = Client()

with open("milestone1_todos.json") as f:
    data = json.load(f)

dataset = client.create_dataset(
    dataset_name="mileston4",
    description="Evaluation dataset for task decomposition accuracy"
)

for user_query, expected_todos in data:
    client.create_example(
        inputs={"query": user_query},
        outputs={"todos": expected_todos},
        dataset_id=dataset.id,
    )

print("Dataset created:", dataset.name)
