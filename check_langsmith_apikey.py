from dotenv import load_dotenv
import os

load_dotenv()

print("LANGSMITH_API_KEY:", os.getenv("LANGSMITH_API_KEY"))
print("LANGCHAIN_API_KEY:", os.getenv("LANGCHAIN_API_KEY"))
