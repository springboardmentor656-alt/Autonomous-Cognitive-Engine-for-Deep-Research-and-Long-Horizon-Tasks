"""
Quick test to verify the agent is working
Tests both tool-based and structured output approaches
"""

from config.settings import settings
from state.agent_state import create_initial_state

print("Testing Financial Planning Agent\n")

settings.validate()

query = "I'm 30 years old and want to save for retirement. Help me plan."

print("=" * 70)
print("APPROACH 1: Structured Output (More Reliable)")
print("=" * 70)
print(f"\nQuery: {query}")
print("\nRunning agent with structured output...\n")

try:
    from agents.structured_output_agent import structured_agent
    
    state = create_initial_state(query, max_iterations=5)
    result = structured_agent.invoke(state)
    
    print("\nResults:")
    print(f"TODOs created: {len(result['todos'])}")
    
    if result['todos']:
        print("\nGenerated Tasks:")
        for todo in result['todos']:
            print(f"  {todo['id'] + 1}. {todo['description']}")
        print("\nSUCCESS with structured output!")
    else:
        print("\nNo tasks generated")
        
except Exception as e:
    print(f"\nERROR: {type(e).__name__}")
    print(f"Message: {str(e)}")

print("\n" + "=" * 70)
print("APPROACH 2: Tool-Based (Original)")
print("=" * 70)
print(f"\nQuery: {query}")
print("\nRunning agent with tool calling...\n")

try:
    from agents.main_agent import financial_agent
    
    state = create_initial_state(query, max_iterations=5)
    result = financial_agent.invoke(state)
    
    print("\nResults:")
    print(f"Iterations: {result['iteration_count']}/{result['max_iterations']}")
    print(f"TODOs created: {len(result['todos'])}")
    
    if result['todos']:
        print("\nGenerated Tasks:")
        for todo in result['todos']:
            print(f"  {todo['id'] + 1}. {todo['description']}")
        print("\nSUCCESS with tool calling!")
    else:
        print("\nNo tasks generated with tool approach")
        
except Exception as e:
    print(f"\nERROR: {type(e).__name__}")
    print(f"Message: {str(e)[:200]}...")
    
    if "tool_use_failed" in str(e):
        print("\nThis is the Groq tool formatting issue.")
        print("Use APPROACH 1 (structured output) instead!")

print("\n" + "=" * 70)
print("RECOMMENDATION")
print("=" * 70)
print("""
APPROACH 1 (Structured Output) is more reliable with Groq.

To use it by default, add to your .env:
PROMPT_STYLE=structured

Or run:
python main.py --interactive

The code will automatically use structured output!
""")

print("Check traces at: https://smith.langchain.com/")
print("=" * 70)