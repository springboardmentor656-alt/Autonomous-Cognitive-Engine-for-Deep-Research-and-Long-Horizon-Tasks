from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

judge_prompt = ChatPromptTemplate.from_template(
    """
You are an evaluator.

Evaluate the following research output based on:
- Clarity
- Coverage
- Structure
- Accuracy

Give one rating: Excellent, Good, Average, or Poor.

Output:
{output}
"""
)

judge_chain = judge_prompt | llm


def judge_output(text: str) -> str:
    return judge_chain.invoke({"output": text}).content
