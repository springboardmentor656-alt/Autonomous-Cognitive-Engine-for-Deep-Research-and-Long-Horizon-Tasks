import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.graph import build_graph

app = build_graph()

tasks = open("evaluation/tasks.txt").read().splitlines()

results = []

for task in tasks:
    output = app.invoke({
        "task": task,
        "todos": [],
        "files": {},
        "final_output": ""
    })

    results.append({
        "task": task,
        "output": output["final_output"]
    })

print("Evaluation runs completed:", len(results))
