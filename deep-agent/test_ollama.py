
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3")

response = llm.invoke("Become a data engineer")
print(response)
