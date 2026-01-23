
from langchain_ollama import OllamaLLM
from langsmith import traceable

llm = OllamaLLM(model="llama3")

@traceable(run_type="llm")
def run(inputs: dict):
    response = llm.invoke(inputs["input"])
    return {"output": response}

if __name__ == "__main__":
    print(run({"input": "Become a data engineer"}))
