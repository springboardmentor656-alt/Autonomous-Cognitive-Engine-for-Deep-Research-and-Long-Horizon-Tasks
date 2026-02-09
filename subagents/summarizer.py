from langchain_groq import ChatGroq
from langsmith import traceable

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

@traceable(name="Summarization Agent")
def run(task: str) -> str:
    """
    Specialized sub-agent that summarizes content.
    """
    prompt = f"""
You are a summarization agent.

Task:
{task}

If no article content is provided, clearly say so.
Otherwise, return a concise summary.
"""
    response = llm.invoke(prompt)
    return response.content

