import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def load_report():
    with open("final_report.md", "r", encoding="utf-8") as f:
        return f.read()


def evaluate_report(report_text: str):

    prompt = f"""
You are a professional AI research evaluator.

Evaluate the following industry report using this rubric:

Score each from 1 (poor) to 5 (excellent):

1. Accuracy – Is the information logically sound?
2. Completeness – Does it address the full objective?
3. Structure – Is it professionally formatted and organized?

Return ONLY valid JSON:

{{
  "accuracy": number,
  "completeness": number,
  "structure": number,
  "overall_score": number,
  "feedback": "Short professional feedback"
}}

REPORT:
\"\"\"
{report_text}
\"\"\"
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=700,
    )

    raw = completion.choices[0].message.content.strip()

    try:
        return json.loads(raw)
    except:
        return {"error": "Invalid JSON", "raw_output": raw}


if __name__ == "__main__":
    report = load_report()
    evaluation = evaluate_report(report)

    print("\nEvaluation Results:\n")
    print(json.dumps(evaluation, indent=2))
