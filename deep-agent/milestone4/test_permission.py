from langsmith import Client

client = Client()

# This should NOT error
datasets = list(client.list_datasets(limit=5))
print(datasets)
