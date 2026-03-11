from agent.supervisor import supervisor_agent
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Configure LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "autonomous-cognitive-engine"


def _get_user_task() -> str:
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()
    return input("Enter a complex task: ").strip()


def _save_results(files: dict[str, str], output_dir: str = "output") -> None:
    os.makedirs(output_dir, exist_ok=True)
    for filename, content in files.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)


def main():

    if not os.environ.get("NEBIUS_API_KEY"):
        print("ERROR: NEBIUS_API_KEY not found in environment.")
        print("Please create a .env file with your API keys.")
        print("See .env.example for the required format.")
        return
    
    user_task = _get_user_task()

    if not user_task:
        print("No task provided. Exiting.")
        return

    try:
        final_state = supervisor_agent(user_task)

        print("\nGenerated files:")
        for filename in sorted(final_state["files"].keys()):
            print(f"- {filename}")

        save = input("\nSave results to disk? (y/n): ").strip().lower()
        if save == "y":
            _save_results(final_state["files"])
            print("Results saved to output/")

    except KeyboardInterrupt:
        print("\nTask interrupted by user.")
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()