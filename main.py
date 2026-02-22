from dotenv import load_dotenv
load_dotenv()

import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "milestone4-master-architect"

from agent_state import default_state
from deep_agent import build_master_agent
from evaluation.reviewer import review_report


if __name__ == "__main__":

    task = input("Enter complex research goal: ")

    agent = build_master_agent()

    state = default_state(task)

    result = agent.invoke(state)

    print("\n===== FINAL REPORT =====\n")
    print(result["final_report"])

    print("\n===== REVIEW =====\n")
    print(review_report(result["final_report"]))
