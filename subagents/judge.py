from langchain_groq import ChatGroq
from langsmith import traceable

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


@traceable(name="Evaluation Judge Agent")
def run(task: str, output: str) -> dict:
    """
    Evaluates the final output quality.
    Returns structured score and feedback.
    """

    prompt = f"""
You are an AI evaluation judge.

Evaluate the following response based on:

1. Instruction Following (Did it complete the task?)
2. Completeness
3. Clarity
4. Structure
5. Relevance

Give:
- Score from 1 to 10
- Short explanation
- Identify missing elements if any

TASK:
{task}

OUTPUT:
{output}

Return in this format:

Score: X/10
Feedback: <your explanation>
"""

    response = llm.invoke(prompt).content

    return {"evaluation": response}
