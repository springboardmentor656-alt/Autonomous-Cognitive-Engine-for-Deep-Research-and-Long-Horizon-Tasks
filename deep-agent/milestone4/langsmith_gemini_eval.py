from langchain_google_genai import ChatGoogleGenerativeAI

judge = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0
)


def evaluate_report(report: str):

    rubric = """
    Evaluate this report from 1-5 on:
    Accuracy, Completeness, Structure, Depth, Professional Tone.

    Return:
    Accuracy: X/5
    Completeness: X/5
    Structure: X/5
    Depth: X/5
    Tone: X/5
    Overall: X/5
    """

    response = judge.invoke(rubric + "\n\nREPORT:\n" + report)

    return response.content
