from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

llm = Ollama(model="tinyllama")

prompt = PromptTemplate.from_template(
    "Create a TODO list for: {task}"
)

chain = prompt | llm

result = chain.invoke({"task": "I want to learn python from scratch"})

print(result)
