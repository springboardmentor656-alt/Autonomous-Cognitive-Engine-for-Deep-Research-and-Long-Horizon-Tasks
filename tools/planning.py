from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

prompt = PromptTemplate(
    input_variables=["task"],
    template="""
You are an expert AI task planner.

Break the following task into 5–7 clear, meaningful subtasks.

Task:
{task}

Return ONLY a numbered list.
"""
)

def write_todos(task: str):
    response = llm.invoke(prompt.format(task=task))
    lines = response.content.strip().split("\n")

    todos = []
    for line in lines:
        if line.strip() and line.strip()[0].isdigit():
            todos.append(line.strip())

    return todos
