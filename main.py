"""
Financial Planning AI Agent - Main Entry Point

This is the command-line interface for interacting with the agent.
"""

import argparse
from config.settings import settings
from state.agent_state import create_initial_state

def get_agent():
    """Get the appropriate agent based on configuration"""
    agent_type = settings.PROMPT_STYLE
    
    if agent_type == "structured":
        from agents.structured_output_agent import structured_agent
        return structured_agent
    else:
        from agents.main_agent import financial_agent
        return financial_agent

def run_interactive():
    """Run agent in interactive mode"""
    print("=" * 70)
    print("FINANCIAL PLANNING AI AGENT")
    print("=" * 70)
    print("\nMilestone 1: Task Planning Demo")
    print("This agent will break down your financial planning request into tasks.\n")
    
    agent = get_agent()
    
    while True:
        user_input = input("\nEnter your financial planning question (or 'quit' to exit):\n> ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
        
        if not user_input.strip():
            continue
        
        print("\nThinking...")
        
        try:
            state = create_initial_state(user_input, max_iterations=5)
            result = agent.invoke(state)
            print("\n" + "=" * 70)
            print("GENERATED TASK PLAN")
            print("=" * 70)
            if result['todos']:
                for todo in result['todos']:
                    print(f"\n{todo['id'] + 1}. {todo['description']}")
                    print(f"   Status: {todo['status']}")
            else:
                print("No tasks generated. Try rephrasing your question.")
            
            print("\n" + "=" * 70)
            print(f"Total iterations: {result['iteration_count']}")
            print(f"View detailed trace at: https://smith.langchain.com/")
            print("=" * 70)
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again with a different question.")

def run_single_query(query: str):
    """Run agent on a single query"""
    print(f"\nProcessing query: {query}\n")
    
    agent = get_agent()
    state = create_initial_state(query, max_iterations=5)
    result = agent.invoke(state)
    
    print("Generated Tasks:")
    for todo in result['todos']:
        print(f"  {todo['id'] + 1}. {todo['description']}")
    
    print(f"\nCompleted in {result['iteration_count']} iterations")

def main():
    parser = argparse.ArgumentParser(
        description="Financial Planning AI Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --interactive
  python main.py --query "Help me plan for retirement"
  python main.py --eval
        """
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--query', '-q',
        type=str,
        help='Run a single query'
    )
    
    parser.add_argument(
        '--eval', '-e',
        action='store_true',
        help='Run evaluation suite'
    )
    
    args = parser.parse_args()
    
    try:
        settings.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nPlease set up your .env file with required API keys.")
        return
    if args.eval:
        from tests.evaluation import run_evaluation
        print("\nRunning full evaluation suite...\n")
        run_evaluation()
    elif args.query:
        run_single_query(args.query)
    elif args.interactive:
        run_interactive()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()