rt os
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

    # Take 3 tasks from user
    print("\n👉 Enter 3 tasks to process:")
    tasks = []
    for i in range(1, 4):
        t = input(f"   Task {i}: ").strip()
        if t:
            tasks.append(t)
        else:
            # Fallback if empty
            tasks.append(f"Task {i}")

    print(f"\nProcessing tasks: {tasks}")

    # Create initial agent state
    state = create_initial_state(tasks=tasks)

    # Invoke LangGraph agent
    # 🔥 This creates a LangSmith RUN
    result = app.invoke(state)

    print("\n" + "=" * 60)
    print("✅ FINAL COMBINED SUMMARY")
    print("=" * 60)
    print(result.get("final_output", "No output generated."))


if __name__ == "__main__":
    main()
