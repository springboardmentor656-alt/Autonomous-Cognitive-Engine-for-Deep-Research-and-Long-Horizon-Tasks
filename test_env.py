import os
from dotenv import load_dotenv

load_dotenv()

print("GROQ_API_KEY set:", bool(os.getenv("GROQ_API_KEY")))
print("TAVILY_API_KEY set:", bool(os.getenv("TAVILY_API_KEY")))
print("LANGCHAIN_API_KEY set:", bool(os.getenv("LANGCHAIN_API_KEY")))
print("LANGCHAIN_PROJECT:", os.getenv("LANGCHAIN_PROJECT"))
