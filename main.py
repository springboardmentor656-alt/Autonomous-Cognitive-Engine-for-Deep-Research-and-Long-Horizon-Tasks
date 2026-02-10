from dotenv import load_dotenv
load_dotenv()

from agent import app
from state import AgentState

if __name__ == "__main__":
    user_input = input("🧠 Enter your goal: ")

    state: AgentState = {
        "user_input": user_input,
        "todos": [],
        "delegated_results": {}
    }

    result = app.invoke(state)

    print("\n✅ FINAL OUTPUT\n")

    for task, output in result["delegated_results"].items():
        print(f"🔹 {task}")
        print(output)
        print()
