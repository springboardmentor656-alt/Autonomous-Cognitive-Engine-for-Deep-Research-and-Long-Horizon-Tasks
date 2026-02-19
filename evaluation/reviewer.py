from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os


def evaluate_report(report_text: str):

    judge = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are an expert research evaluator.

Score this report from 1-5 on:

1. Accuracy
2. Completeness
3. Structure

Return strictly in this format:

Accuracy: X/5
Completeness: X/5
Structure: X/5

Report:
{report}
"""
    )

    chain = prompt | judge
    # Truncate report to avoid token overflow
    MAX_CHARS = 4000  # Safe for 8b model

    short_report = report_text[:MAX_CHARS]

    result = chain.invoke({"report": short_report})


    return result.content
