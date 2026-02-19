from dotenv import load_dotenv
load_dotenv()

from langsmith import Client

client = Client()

DATASET_NAME = "autonomous_research_eval"

# Create dataset only if it doesn't exist
try:
    client.read_dataset(dataset_name=DATASET_NAME)
    print(f"Dataset '{DATASET_NAME}' already exists")
except Exception:
    client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Evaluation dataset for autonomous research agent"
    )
    print(f"Dataset '{DATASET_NAME}' created")
