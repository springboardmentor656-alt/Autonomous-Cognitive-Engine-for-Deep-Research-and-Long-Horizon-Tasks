from agent.graph import build_graph
from evaluation.reviewer import evaluate_report

app = build_graph()

task = input("Enter a complex task: ")

# Invoke agent
state = app.invoke(
    {
        "task": task,
        "todos": [],
        "files": {},
        "current_step": 0,
        "next_action": "",
        "final_output": ""
    },
    config={"recursion_limit": 200}
)



# 🔹 Extract plan
plan = state.get("todos") or []

# 🔹 Extract final synthesized output
final_output = state.get("final_output", "NO FINAL OUTPUT GENERATED")

# 🔹 Print Plan
print("\n--- TODOs (PLAN) ---")
for t in plan:
    print("-", t)

# 🔹 Print Final Output
print("\n--- FINAL OUTPUT ---")
print(final_output)

# ==============================
# ✅ ADD REVIEWER HERE
# ==============================

if final_output and final_output != "NO FINAL OUTPUT GENERATED":
    print("\n--- LLM REVIEW SCORES ---")
    review_scores = evaluate_report(final_output[:4000])

    print(review_scores)
else:
    print("\nNo report generated. Skipping evaluation.")

# ==============================
# For LangSmith evaluation
# ==============================

result_for_eval = {
    "inputs": task,
    "outputs": final_output,
    "plan": plan
}
