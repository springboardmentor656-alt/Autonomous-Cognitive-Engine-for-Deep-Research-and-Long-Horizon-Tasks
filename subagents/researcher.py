from langchain_groq import ChatGroq
from langsmith import traceable

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.4
)


@traceable(name="Research Agent")
def run(task: str) -> str:
    prompt = f"""
You are a professional research analyst.

Perform detailed research on:

{task}

Provide:
- Key findings
- Explanations
- Important insights
"""

    response = llm.invoke(prompt)
    return response.content
