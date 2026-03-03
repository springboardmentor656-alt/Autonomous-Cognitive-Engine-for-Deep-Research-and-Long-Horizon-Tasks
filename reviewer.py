import os
from langchain_groq import ChatGroq

# Setup the Judge using a powerful model [cite: 43, 61]
G_KEY = "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"
judge_llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=G_KEY)

def evaluate_report():
    print("🕵️  STARTING TASK 4: LLM-AS-A-JUDGE EVALUATION...")
    
    try:
        with open("final_report.md", "r", encoding="utf-8") as f:
            report_content = f.read()
    except FileNotFoundError:
        print("❌ Run main.py first to generate a report!")
        return

    # The Rubric requested by your mentor
    rubric_prompt = f"""
    You are an expert reviewer. Evaluate the report below using this rubric (Score 1-5):

    1. Accuracy: Is the information factually correct?
    2. Completeness: Did it address all parts of the research topic and TODO list? [cite: 7, 122]
    3. Structure: Is the report professionally formatted in Markdown? 

    REPORT CONTENT:
    {report_content}
    
    Provide the scores and a final justification.
    """

    evaluation = judge_llm.invoke(rubric_prompt)
    
    print("\n" + "="*40)
    print("⭐ FINAL SCORECARD ⭐")
    print("="*40)
    print(evaluation.content)
    
    with open("evaluation_results.txt", "w", encoding="utf-8") as f:
        f.write(evaluation.content)
    print("\n✅ Evaluation results saved to 'evaluation_results.txt'")

if __name__ == "__main__":
    evaluate_report()