from agent.graph import build_graph

app = build_graph()

task = input("Enter a complex task: ")

# Invoke agent
state = app.invoke({
    "task": task,
    "todos": [],
    "files": {}
})

# 🔹 Extract plan
plan = state.get("todos") or []

# 🔹 Extract final synthesized output (IMPORTANT)
final_output = state.get("final_output", "NO FINAL OUTPUT GENERATED")

# 🔹 Print for user
print("\n--- TODOs (PLAN) ---")
for t in plan:
    print("-", t)

print("\n--- FINAL OUTPUT ---")
print(final_output)

# 🔹 Structure expected by LangSmith evaluators
result_for_eval = {
    "inputs": task,
    "outputs": final_output,
    "plan": plan
}

# Optional: return when used inside evaluation runner
# return result_for_eval
