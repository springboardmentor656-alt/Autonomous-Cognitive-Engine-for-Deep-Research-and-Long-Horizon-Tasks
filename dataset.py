# dataset.py

from dotenv import load_dotenv
import os
from langsmith.client import Client

load_dotenv()

client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))

DATASET_NAME = "ds-granular-oleo-34"

existing = [d.name for d in client.list_datasets()]
if DATASET_NAME not in existing:
    client.create_dataset(name=DATASET_NAME)
    print(f"Dataset '{DATASET_NAME}' created.")
else:
    print(f"Dataset '{DATASET_NAME}' already exists.")


