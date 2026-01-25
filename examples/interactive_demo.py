"""
Fixed Interactive CLI demo for Milestone 2 agent.
Now properly shows files with 'files' command!
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graph import create_agent_graph, run_agent
from src.state import AgentState
from langchain_core.messages import AIMessage, HumanMessage


def display_banner():
    """Display welcome banner."""
    print("\n" + "="*80)
    print("🤖 MILESTONE 2: Context Offloading Agent - Interactive Demo")
    print("="*80)
    print("\nFeatures:")
    print("  ✅ Virtual file system (ls, read_file, write_file, edit_file)")
    print("  ✅ Automatic context offloading for long tasks")
    print("  ✅ Multi-step task handling")
    print("\nCommands:")
    print("  'files' - Show all files in the virtual file system")
    print("  'clear' - Clear conversation (keeps files)")
    print("  'reset' - Reset everything (clears files too)")
    print("  'test' - Run a sample test scenario")
    print("  'save' - Save files to disk")
    print("  'exit' or 'quit' - Exit the program")
    print("="*80 + "\n")


def display_files(state: AgentState):
    """Display all files in the virtual file system."""
    files = state['files']
    
    print(f"\n{'='*80}")
    print(f"📁 VIRTUAL FILE SYSTEM")
    print(f"{'='*80}")
    
    if not files:
        print("❌ No files in the system yet.")
        print("\nTo create files, ask the agent:")
        print('  Example: "Create a file called test.txt with content Hello World"')
        print(f"{'='*80}\n")
        return
    
    print(f"\nTotal files: {len(files)}")
    print(f"{'─'*80}")
    
    for filename, content in files.items():
        print(f"\n📄 {filename}")
        print(f"   Size: {len(content)} characters")
        print(f"   Preview: {content[:80]}{'...' if len(content) > 80 else ''}")
    
    print(f"\n{'─'*80}")
    print(f"💡 Use 'save' to export these files to disk")
    print(f"{'='*80}\n")


def save_files_to_disk(state: AgentState):
    """Save virtual files to actual disk."""
    files = state['files']
    
    if not files:
        print("\n❌ No files to save!\n")
        return
    
    # Create output directory
    output_dir = "results/interactive_files"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save each file
    for filename, content in files.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Saved: {filepath}")
    
    print(f"\n💾 All {len(files)} files saved to: {output_dir}\n")


def run_test_scenario(graph, state):
    """Run a sample test scenario."""
    test_input = """Please help me with this task:

I need to create 3 product summaries:

Product A: Laptop X - $999, 16GB RAM, 512GB SSD, Intel i7
Product B: Laptop Y - $799, 8GB RAM, 256GB SSD, Intel i5
Product C: Laptop Z - $1299, 32GB RAM, 1TB SSD, Intel i9

Tasks:
1. Create a summary for each product and save to: product_a.txt, product_b.txt, product_c.txt
2. Use ls() to verify all files were created
3. Read each product file
4. Create a comparison document and save to: comparison.txt
5. Show me the final comparison

Please use write_file() to save each summary!"""
    
    print("\n🧪 Running test scenario: Product Comparison")
    print("─"*80)
    print("This will demonstrate:")
    print("  • Creating multiple files")
    print("  • Using ls() to list files")
    print("  • Reading saved files")
    print("  • Creating a synthesis document")
    print("─"*80 + "\n")
    
    return run_agent(graph, test_input, state)


def main():
    """Main interactive loop."""
    
    # Load environment
    load_dotenv()
    
    # Check API key
    if not os.getenv("GROQ_API_KEY"):
        print("\n❌ ERROR: GROQ_API_KEY not found!")
        print("\nPlease create a .env file with:")
        print("GROQ_API_KEY=your-key-here")
        return
    
    display_banner()
    
    # Create agent
    print("Initializing agent...")
    try:
        graph = create_agent_graph()
        print("✅ Agent ready!\n")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}\n")
        import traceback
        traceback.print_exc()
        return
    
    # Initialize state
    state = AgentState(
        messages=[],
        files={},
        intermediate_steps=[]
    )
    
    print("💡 Try: 'Create a file called notes.txt with content: This is my first note'")
    print("💡 Then type: 'files' to see your created file\n")
    
    # Main loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['exit', 'quit']:
                print("\n👋 Goodbye!\n")
                break
            
            if user_input.lower() == 'files':
                display_files(state)
                continue
            
            if user_input.lower() == 'save':
                save_files_to_disk(state)
                continue
            
            if user_input.lower() == 'clear':
                state['messages'] = []
                state['intermediate_steps'] = []
                print("\n🗑️  Conversation cleared (files preserved)\n")
                continue
            
            if user_input.lower() == 'reset':
                state = AgentState(messages=[], files={}, intermediate_steps=[])
                print("\n🗑️  Everything reset (files deleted)\n")
                continue
            
            if user_input.lower() == 'test':
                state = run_test_scenario(graph, state)
                
                # Display final response
                for msg in reversed(state['messages']):
                    if isinstance(msg, AIMessage) and msg.content:
                        print(f"\n🤖 Agent: {msg.content}\n")
                        break
                
                # Show files created
                print(f"\n📊 Files created during test: {len(state['files'])}")
                if state['files']:
                    print("Type 'files' to see them!\n")
                continue
            
            # Process regular input
            print("\n🤔 Agent working...\n")
            
            try:
                state = run_agent(graph, user_input, state)
                
                # Display response
                for msg in reversed(state['messages']):
                    if isinstance(msg, AIMessage) and msg.content:
                        print(f"🤖 Agent: {msg.content}\n")
                        break
                
                # Show file count if files were created
                if state['files']:
                    print(f"📁 Current files: {len(state['files'])} (type 'files' to view)\n")
                
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
                import traceback
                traceback.print_exc()
            
            print("─"*80)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()