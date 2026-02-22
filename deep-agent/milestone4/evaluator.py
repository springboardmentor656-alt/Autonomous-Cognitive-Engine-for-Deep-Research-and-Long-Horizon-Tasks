from langchain_ollama import ChatOllama

judge_llm = ChatOllama(model="llama3", temperature=0)


def evaluate_report(report_text: str) -> int:
    """
    Returns ONLY an integer score from 1 to 10.
    """

    prompt = f"""
You are grading a report.

Give an overall score from 1 to 10.

Respond with ONLY a single number.
Do NOT explain.

Report:
{report_text}
"""

    response = judge_llm.invoke(prompt)

    try:
        score = int(response.content.strip())
        return score
    except:
        return 0
