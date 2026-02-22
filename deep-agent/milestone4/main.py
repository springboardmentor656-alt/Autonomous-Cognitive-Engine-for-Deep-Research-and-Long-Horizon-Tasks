from dotenv import load_dotenv
load_dotenv()

from agent.graph import app
from evaluator import evaluate_report

initial_state = {
    "messages": [
        {"role": "user", "content": "Write a research report on green hydrogen"}
    ],
    "todos": [],
    "files": {},
    "current_task": "",
    "completed": False
}

result = app.invoke(initial_state)

final_report = result["files"]["final_report.txt"]

print("FINAL REPORT:\n")
print(final_report)

print("\nEVALUATION:\n")
print(evaluate_report(final_report))
