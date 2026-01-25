# ============================================================================
# FILE: working_agent.py
# Complete working solution in ONE file for easy setup
# ============================================================================

import os
import re
from typing import TypedDict, Dict, List, Literal, Annotated
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

# Load environment
load_dotenv()

# ============================================================================
# STATE DEFINITION
# ============================================================================

class AgentState(TypedDict):
    """State with messages and virtual file system."""
    messages: Annotated[List[BaseMessage], add_messages]
    files: Dict[str, str]
    intermediate_steps: List[Dict[str, str]]

# ============================================================================
# VIRTUAL FILE SYSTEM (Simple in-memory implementation)
# ============================================================================

class VirtualFileSystem:
    """Simple file system for context offloading."""
    
    def __init__(self, state: AgentState):
        self.state = state
    
    def ls(self) -> str:
        """List all files."""
        files = self.state['files']
        if not files:
            return "📁 No files in the file system."
        file_list = "\n".join([f"  • {filename} ({len(content)} chars)" 
                               for filename, content in files.items()])
        return f"📁 Files in system ({len(files)} total):\n{file_list}"
    
    def read_file(self, filename: str) -> str:
        """Read a file."""
        files = self.state['files']
        if filename not in files:
            available = ", ".join(files.keys()) if files else "none"
            return f"❌ Error: File '{filename}' not found. Available: {available}"
        return f"📄 Content of '{filename}':\n{files[filename]}"
    
    def write_file(self, filename: str, content: str) -> str:
        """Write to a file."""
        self.state['files'][filename] = content
        self.state['intermediate_steps'].append({
            'tool': 'write_file',
            'filename': filename,
            'size': len(content)
        })
        return f"✅ Successfully wrote {len(content)} characters to '{filename}'"
    
    def edit_file(self, filename: str, new_content: str) -> str:
        """Edit an existing file."""
        files = self.state['files']
        if filename not in files:
            return f"❌ Error: File '{filename}' not found. Use write_file to create it."
        old_size = len(files[filename])
        files[filename] = new_content
        self.state['intermediate_steps'].append({
            'tool': 'edit_file',
            'filename': filename,
            'old_size': old_size,
            'new_size': len(new_content)
        })
        return f"✅ Successfully edited '{filename}' (was {old_size} chars, now {len(new_content)} chars)"

# ============================================================================
# AGENT FUNCTIONS
# ============================================================================

def parse_tool_call(text: str) -> tuple:
    """Parse tool call from agent's response."""
    # Look for patterns like:
    # - write_file("filename.txt", "content")
    # - read_file("filename.txt")
    # - ls()
    # - edit_file("filename.txt", "new content")
    
    # Pattern for write_file
    write_pattern = r'write_file\(["\']([^"\']+)["\'],\s*["\'](.+?)["\']\)'
    write_match = re.search(write_pattern, text, re.DOTALL)
    if write_match:
        return ('write_file', {'filename': write_match.group(1), 'content': write_match.group(2)})
    
    # Pattern for read_file
    read_pattern = r'read_file\(["\']([^"\']+)["\']\)'
    read_match = re.search(read_pattern, text)
    if read_match:
        return ('read_file', {'filename': read_match.group(1)})
    
    # Pattern for edit_file
    edit_pattern = r'edit_file\(["\']([^"\']+)["\'],\s*["\'](.+?)["\']\)'
    edit_match = re.search(edit_pattern, text, re.DOTALL)
    if edit_match:
        return ('edit_file', {'filename': edit_match.group(1), 'new_content': edit_match.group(2)})
    
    # Pattern for ls
    if 'ls()' in text or 'list files' in text.lower():
        return ('ls', {})
    
    return (None, None)

def create_agent_graph():
    """Create the LangGraph workflow."""
    
    # Initialize LLM
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    # System prompt
    SYSTEM_PROMPT = """You are an AI assistant with a virtual file system.

IMPORTANT: For multi-step tasks, you MUST use the file system to save intermediate results.

Available commands (use these EXACTLY as shown):
- write_file("filename.txt", "content here") - Save content to a file
- read_file("filename.txt") - Read a file's content
- ls() - List all files
- edit_file("filename.txt", "new content") - Edit an existing file

CRITICAL WORKFLOW for multi-step tasks:
1. For each item/step, write_file() to save the result
2. After saving all items, use ls() to verify
3. Use read_file() to retrieve saved files
4. Create final synthesis and save with write_file()

Example for "Summarize 3 articles":
Step 1: Create summary for article 1 → write_file("summary1.txt", "summary content")
Step 2: Create summary for article 2 → write_file("summary2.txt", "summary content")
Step 3: Create summary for article 3 → write_file("summary3.txt", "summary content")
Step 4: Verify → ls()
Step 5: Read summaries → read_file("summary1.txt"), read_file("summary2.txt"), read_file("summary3.txt")
Step 6: Create final → write_file("final.txt", "combined summary")

ALWAYS use write_file() to save each intermediate result!"""
    
    # Agent node
    def agent_node(state: AgentState) -> AgentState:
        """Agent makes decisions."""
        messages = state['messages']
        
        # Add system prompt on first call
        if len(messages) == 1:
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
        # Get LLM response
        response = llm.invoke(messages)
        
        return {"messages": [response]}
    
    # Tools node
    def tools_node(state: AgentState) -> AgentState:
        """Execute tool calls."""
        messages = state['messages']
        last_message = messages[-1]
        
        if not isinstance(last_message, AIMessage):
            return {"messages": []}
        
        content = last_message.content
        fs = VirtualFileSystem(state)
        
        # Parse and execute tool calls
        tool_name, tool_args = parse_tool_call(content)
        
        if tool_name:
            print(f"  🔧 Executing: {tool_name}({tool_args})")
            
            try:
                if tool_name == 'ls':
                    result = fs.ls()
                elif tool_name == 'read_file':
                    result = fs.read_file(tool_args['filename'])
                elif tool_name == 'write_file':
                    result = fs.write_file(tool_args['filename'], tool_args['content'])
                elif tool_name == 'edit_file':
                    result = fs.edit_file(tool_args['filename'], tool_args['new_content'])
                else:
                    result = f"Unknown tool: {tool_name}"
                
                print(f"     ✅ {result[:100]}")
                
                # Add result as a message
                return {"messages": [HumanMessage(content=f"Tool result: {result}")]}
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                print(f"     {error_msg}")
                return {"messages": [HumanMessage(content=f"Tool error: {error_msg}")]}
        
        return {"messages": []}
    
    # Router
    def should_continue(state: AgentState) -> Literal["tools", "end"]:
        """Decide whether to continue or end."""
        last_message = state['messages'][-1]
        
        if isinstance(last_message, AIMessage):
            content = last_message.content
            # Check if there's a tool call
            tool_name, _ = parse_tool_call(content)
            if tool_name:
                return "tools"
        
        return "end"
    
    # Build graph
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tools_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()

# ============================================================================
# TEST SCENARIOS
# ============================================================================

TEST_SCENARIOS = {
    "simple": """Create 3 summary files:
1. write_file("summary1.txt", "AI summary")
2. write_file("summary2.txt", "ML summary")  
3. write_file("summary3.txt", "DL summary")
4. Then ls() to verify
5. Read all files and create final combined summary in "final.txt"
""",
    
    "multi_article": """Summarize these 3 articles and save each:

Article 1 (AI): Artificial intelligence is transforming industries through automation and data analysis.
Article 2 (ML): Machine learning enables systems to learn from data without explicit programming.
Article 3 (DL): Deep learning uses neural networks to process complex patterns in data.

Tasks:
1. Create summary for each → write_file("summary_article1.txt", ...), write_file("summary_article2.txt", ...), write_file("summary_article3.txt", ...)
2. Verify with ls()
3. Read all summaries
4. Create combined report → write_file("final_report.txt", ...)
"""
}

# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

def run_test(test_name: str = "simple"):
    """Run a test scenario."""
    print(f"\n{'='*80}")
    print(f"Running Test: {test_name}")
    print(f"{'='*80}\n")
    
    graph = create_agent_graph()
    state = AgentState(messages=[], files={}, intermediate_steps=[])
    
    # Add test input
    state['messages'].append(HumanMessage(content=TEST_SCENARIOS[test_name]))
    
    # Run graph
    final_state = graph.invoke(state, {"recursion_limit": 30})
    
    # Show results
    print(f"\n{'='*80}")
    print("RESULTS:")
    print(f"{'='*80}")
    print(f"Files created: {len(final_state['files'])}")
    print(f"write_file calls: {sum(1 for s in final_state['intermediate_steps'] if s.get('tool') == 'write_file')}")
    print(f"\nFiles:")
    for filename, content in final_state['files'].items():
        print(f"  • {filename} ({len(content)} chars)")
    print(f"{'='*80}\n")

def run_interactive():
    """Run interactive mode."""
    print("\n🤖 Interactive Agent (type 'exit' to quit, 'test' for demo)\n")
    
    graph = create_agent_graph()
    state = AgentState(messages=[], files={}, intermediate_steps=[])
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            break
        
        if user_input.lower() == 'test':
            user_input = TEST_SCENARIOS['simple']
        
        if user_input.lower() == 'files':
            fs = VirtualFileSystem(state)
            print(f"\n{fs.ls()}\n")
            continue
        
        state['messages'].append(HumanMessage(content=user_input))
        state = graph.invoke(state, {"recursion_limit": 30})
        
        # Get last AI message
        for msg in reversed(state['messages']):
            if isinstance(msg, AIMessage):
                print(f"\nAgent: {msg.content}\n")
                break

if __name__ == "__main__":
    import sys
    
    if not os.getenv("GROQ_API_KEY"):
        print("❌ ERROR: GROQ_API_KEY not found in .env file")
        sys.exit(1)
    
    # Run test or interactive mode
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            run_test("multi_article")
        elif sys.argv[1] == "interactive":
            run_interactive()
    else:
        # Default: run simple test
        run_test("simple")