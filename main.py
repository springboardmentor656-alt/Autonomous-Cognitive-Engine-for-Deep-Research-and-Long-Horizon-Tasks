from dotenv import load_dotenv
load_dotenv()

import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "milestone3-sub-agent"

from deep_agent import build_deep_agent
from Evaluation.delegation_evaluator import evaluate_delegation


if __name__ == "__main__":
    task = input("Enter your task: ")

    results = build_deep_agent(task)

    print("\n================ FINAL RESULTS ================\n")

    for i, item in enumerate(results, 1):
        print(f"{i}. Output:")
        print(item)
        print("-" * 60)

    # ---------- EVALUATION ----------
    metrics = evaluate_delegation(results)

    print("\n========= EVALUATION =========")
    print(f"Total Tasks: {metrics['total_tasks']}")
    print(f"Delegated Tasks: {metrics['successful_delegations']}")
    print(f"Delegation Accuracy: {metrics['delegation_accuracy'] * 100:.2f}%")
