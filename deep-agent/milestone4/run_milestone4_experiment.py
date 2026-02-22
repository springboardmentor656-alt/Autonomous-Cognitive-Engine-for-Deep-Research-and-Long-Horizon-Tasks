from dotenv import load_dotenv
load_dotenv()

import re
from langsmith.evaluation import evaluate
from agent.graph import app
from evaluator import evaluate_report
from langchain_ollama import ChatOllama

# ---------------------------------------------------------
# Local LLaMA Judge Model (Ollama)
# ---------------------------------------------------------
judge_llm = ChatOllama(model="llama3", temperature=0)


# =========================================================
# 1️⃣ Agent Runner
# =========================================================
def agent_runner(example):
    """
    Runs Milestone 4 agent on dataset example.
    Compatible with both dict and Example object.
    """

    # Handle both LangSmith example formats
    if isinstance(example, dict):
        user_input = example["input"]
    else:
        user_input = example.inputs["input"]

    state = {
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "todos": [],
        "files": {},
        "current_task": "",
        "completed": False
    }

    result = app.invoke(state, config={"recursion_limit": 50})

    final_report = result["files"].get("final_report.txt", "")

    return {
        "output": final_report
    }


# =========================================================
# 2️⃣ Judge Evaluator (1–10 Scale)
# =========================================================
def judge(run, example):
    final_output = run.outputs.get("output", "")

    if not final_output:
        return {
            "key": "judge",
            "score": 0,
            "comment": "No output generated"
        }

    overall_score = evaluate_report(final_output)

    return {
        "key": "judge",
        "score": overall_score,
        "comment": f"Overall Score: {overall_score}/10"
    }


# =========================================================
# 3️⃣ Correctness Evaluator (0–1 Scale)
# =========================================================
def correctness(run, example):
    model_output = run.outputs.get("output", "")

    # Get reference output safely
    if isinstance(example, dict):
        reference_output = example.get("output", "")
    else:
        reference_output = example.outputs.get("output", "")

    if not model_output or not reference_output:
        return {
            "key": "correctness",
            "score": 0,
            "comment": "Missing output or reference"
        }

    prompt = f"""
Compare the generated report with the reference report.

Score semantic correctness from 0 to 1.

Return ONLY a decimal number between 0 and 1.
Do NOT explain.

Generated Report:
{model_output}

Reference Report:
{reference_output}
"""

    response = judge_llm.invoke(prompt)
    text = response.content.strip()

    try:
        match = re.search(r"\b(0(\.\d+)?|1(\.0+)?)\b", text)
        if match:
            score = float(match.group(0))
            return {
                "key": "correctness",
                "score": score,
                "comment": f"Correctness score: {score}"
            }
        else:
            return {
                "key": "correctness",
                "score": 0,
                "comment": "Failed to parse correctness score"
            }
    except:
        return {
            "key": "correctness",
            "score": 0,
            "comment": "Error evaluating correctness"
        }


# =========================================================
# 4️⃣ Run Experiment
# =========================================================
if __name__ == "__main__":

    evaluate(
        agent_runner,
        data="milestone4",  # Must exactly match dataset name
        evaluators=[judge, correctness],
        experiment_prefix="milestone4-final"
    )

    print("✅ Milestone 4 experiment completed.")