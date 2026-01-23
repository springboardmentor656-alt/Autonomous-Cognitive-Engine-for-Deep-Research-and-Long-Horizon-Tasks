from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

prompt = ChatPromptTemplate.from_template(
    """
Summarize the following content clearly and concisely:

{content}
"""
)

chain = prompt | llm


def summarization_agent(text: str) -> str:
    return chain.invoke({"content": text}).content
