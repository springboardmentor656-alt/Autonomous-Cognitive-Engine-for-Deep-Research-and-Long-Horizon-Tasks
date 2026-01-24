import os
from dotenv import load_dotenv

from graph.graph import app
from agent.state import create_initial_state


# -------------------------------------------------
# Load environment variables (LangSmith)
# -------------------------------------------------
load_dotenv()

# Enable LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"


def main():
    print("=" * 60)
    print("🚀 Agentic AI – Milestone 2")
    print("3 Summaries → Virtual Files → Final Summary")
    print("=" * 60)

    # Take task from user
    user_task = input("\n👉 Enter your task: ").strip()

    if not user_task:
        print("❌ Task cannot be empty.")
        return

    # Create initial agent state
    state = create_initial_state(task=user_task)

    # Invoke LangGraph agent
    # 🔥 This creates a LangSmith RUN
    result = app.invoke(state)

    print("\n" + "=" * 60)
    print("✅ FINAL COMBINED SUMMARY")
    print("=" * 60)
    print(result.get("final_output", "No output generated."))


if __name__ == "__main__":
    main()
