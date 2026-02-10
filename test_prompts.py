from agent import app

tests = [
    "Autonomous research report on climate change",
    "Refactor a large Python codebase",
    "Market analysis for EV adoption",
    "Literature review on blockchain security",
    "Cloud migration strategy"
]

pass_count = 0

for t in tests:
    result = app.invoke({"messages": [t], "todos": []})
    if len(result["todos"]) >= 5:
        pass_count += 1

print(f"Accuracy: {pass_count}/{len(tests)}")
