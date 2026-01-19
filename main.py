import argparse
import os

from config.settings import settings
from state.agent_state import create_initial_state


def get_agent():
    """Select agent based on PROMPT_STYLE and MILESTONE"""

    agent_type = settings.PROMPT_STYLE
    milestone = os.getenv("MILESTONE", "1")

    print(f"\n[INFO] Using Milestone {milestone} | Mode: {agent_type}")

    if milestone == "2":
        if agent_type == "structured":
            from agents.structured_op_agent_m2 import structured_agent_m2
            return structured_agent_m2
        else:
            from agents.main_agent_m2 import financial_agent_m2
            return financial_agent_m2

    else:
        if agent_type == "structured":
            from agents.structured_output_agent import structured_agent
            return structured_agent
        else:
            from agents.main_agent import financial_agent
            return financial_agent


def run_interactive():
    print("=" * 70)
    print("FINANCIAL PLANNING AI AGENT")
    print("=" * 70)

    agent = get_agent()

    while True:
        user_input = input("\nEnter your financial planning question (or 'quit'): \n> ")

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break

        if not user_input.strip():
            continue

        print("\nThinking...\n")

        try:
            state = create_initial_state(user_input, max_iterations=5)
            result = agent.invoke(state)

            print("\n" + "=" * 70)
            print("GENERATED TASK PLAN")
            print("=" * 70)

            if result.get("todos"):
                for todo in result["todos"]:
                    print(f"\n{todo['id'] + 1}. {todo['description']}")
                    print(f"   Status: {todo['status']}")
            else:
                print("No tasks generated.")
            if result.get("final_output"):
                print("\nFINAL SUMMARY:")
                print(result["final_output"])

            print("\n" + "=" * 70)
            print(f"Iterations: {result['iteration_count']}")
            print("=" * 70)

        except Exception as e:
            print(f"\nError: {str(e)}")


def run_single_query(query: str):
    print(f"\nProcessing query: {query}\n")
    agent = get_agent()
    state = create_initial_state(query, max_iterations=5)
    result = agent.invoke(state)

    print("Generated Tasks:")
    for todo in result.get("todos", []):
        print(f"  {todo['id'] + 1}. {todo['description']}")

    if result.get("files"):
        print("\nSaved Files:")
        for fname in result["files"]:
            print(f" - {fname}")

    print(f"\nCompleted in {result['iteration_count']} iterations")

def main():
    parser = argparse.ArgumentParser(
        description="Financial Planning AI Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--interactive', '-i', action='store_true')
    parser.add_argument('--query', '-q', type=str)
    parser.add_argument('--eval', '-e', action='store_true')

    args = parser.parse_args()

    try:
        settings.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Set your API keys in .env")
        return

    if args.eval:
        from tests.evaluation import run_evaluation
        print("\nRunning evaluation...\n")
        run_evaluation()

    elif args.query:
        run_single_query(args.query)

    elif args.interactive:
        run_interactive()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
