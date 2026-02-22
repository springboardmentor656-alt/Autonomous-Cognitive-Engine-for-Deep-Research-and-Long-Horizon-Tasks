from agent.react_agent import app

print("\n=== Deep Agent — Milestone 2 ===")
print("Type a prompt. Type 'exit' to quit.\n")

while True:
    user_input = input("You > ")
    if user_input.lower() == "exit":
        break

    state = {
        "messages": [{"role": "user", "content": user_input}],
        "todos": [],
        "files": {},
        "needs_read": False
    }

    result = app.invoke(state)

    print("\nGenerated TODOs:\n")
    for t in result["todos"]:
        print(t)
    print("\n--------------------------\n")