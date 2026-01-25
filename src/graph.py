"""
Improved LangGraph workflow with better multi-step handling.
This version explicitly guides the agent through each step.
"""

import os
import json
import re
from typing import Literal
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, END

from src.state import AgentState
from src.tools import all_tools, _current_state


def create_agent_graph():
    """
    Create the LangGraph workflow with improved prompting for multi-step tasks.
    """
    
    # Initialize LLM
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",  # Updated model
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    # Improved system prompt with explicit examples
    SYSTEM_PROMPT = """You are an AI assistant with a virtual file system for managing information.

YOUR CORE TASK: When given multi-step tasks, you MUST save intermediate results to files.

=== AVAILABLE TOOLS ===
Use these EXACT formats:

1. write_file(filename, content) - Save content to a file
   Example: write_file("summary1.txt", "This is the summary of article 1")

2. read_file(filename) - Read a file's content
   Example: read_file("summary1.txt")

3. ls() - List all files
   Example: ls()

4. edit_file(filename, new_content) - Edit existing file
   Example: edit_file("summary1.txt", "Updated summary")

=== CRITICAL WORKFLOW ===

For ANY multi-step task, follow this pattern:

TASK: "Summarize 3 articles and create combined report"

STEP 1: Process article 1
→ write_file("summary_article1.txt", "summary content here")

STEP 2: Process article 2
→ write_file("summary_article2.txt", "summary content here")

STEP 3: Process article 3
→ write_file("summary_article3.txt", "summary content here")

STEP 4: Verify files created
→ ls()

STEP 5: Read saved files
→ read_file("summary_article1.txt")
→ read_file("summary_article2.txt")
→ read_file("summary_article3.txt")

STEP 6: Create combined report
→ write_file("final_report.txt", "combined content")

STEP 7: Respond with final answer

=== RULES ===
1. ALWAYS use write_file() to save each intermediate result
2. Process one item at a time
3. Save after processing each item
4. Use descriptive filenames (e.g., 'summary_article1.txt', not just 'file1.txt')
5. Call ls() to verify files before reading
6. Read saved files with read_file() before creating final output
7. Save final output to a file as well

=== EXAMPLES ===

Example 1: "Create summaries for 3 topics"
→ write_file("topic1_summary.txt", "summary 1")
→ write_file("topic2_summary.txt", "summary 2")
→ write_file("topic3_summary.txt", "summary 3")
→ ls()
→ read_file("topic1_summary.txt")
→ read_file("topic2_summary.txt")
→ read_file("topic3_summary.txt")
→ write_file("combined.txt", "all summaries combined")

Example 2: "Analyze sales data by region"
→ write_file("north_region.txt", "north analysis")
→ write_file("south_region.txt", "south analysis")
→ write_file("east_region.txt", "east analysis")
→ write_file("west_region.txt", "west analysis")
→ ls()
→ write_file("executive_summary.txt", "final analysis")

DO NOT skip steps. DO NOT try to process everything at once.
ALWAYS save intermediate results!"""
    
    # Track which step we're on for complex tasks
    def detect_task_complexity(user_input: str) -> int:
        """Detect how many steps a task requires."""
        # Count mentions of items to process
        patterns = [
            r'(\d+)\s+(articles|topics|items|products|regions)',
            r'(three|four|five|3|4|5)\s+(articles|topics|items)',
        ]
        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                num = match.group(1)
                if num in ['three', '3']: return 3
                if num in ['four', '4']: return 4
                if num in ['five', '5']: return 5
                try:
                    return int(num)
                except:
                    pass
        return 1
    
    # Agent node with enhanced prompting
    def agent_node(state: AgentState) -> AgentState:
        """Agent reasoning node with step tracking."""
        _current_state["state"] = state
        messages = state['messages']
        
        # Add system prompt on first call
        if len(messages) == 1 and isinstance(messages[0], HumanMessage):
            user_input = messages[0].content
            num_steps = detect_task_complexity(user_input)
            
            # Add specific guidance based on complexity
            if num_steps > 1:
                enhanced_prompt = f"""{SYSTEM_PROMPT}

IMPORTANT: This task requires processing {num_steps} items.
You MUST:
1. Process item 1 → write_file()
2. Process item 2 → write_file()
{"3. Process item 3 → write_file()" if num_steps >= 3 else ""}
{"4. Process item 4 → write_file()" if num_steps >= 4 else ""}
{"5. Process item 5 → write_file()" if num_steps >= 5 else ""}
{num_steps + 1}. Use ls() to verify all files
{num_steps + 2}. Read all files with read_file()
{num_steps + 3}. Create combined output → write_file()

START with the FIRST item NOW."""
                messages = [SystemMessage(content=enhanced_prompt)] + messages
            else:
                messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
        # Get response from LLM
        response = llm.invoke(messages)
        
        return {"messages": [response]}
    
    # Tools node - executes tools
    def tools_node(state: AgentState) -> AgentState:
        """Execute tool calls found in agent's response."""
        _current_state["state"] = state
        messages = state['messages']
        last_message = messages[-1]
        
        if not isinstance(last_message, AIMessage):
            return {"messages": []}
        
        content = last_message.content
        tool_outputs = []
        
        # Parse tool calls using multiple strategies
        tool_calls = parse_tool_calls(content)
        
        if tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call['name']
                tool_args = tool_call['args']
                
                print(f"  🔧 Executing: {tool_name}({tool_args})")
                
                # Find and execute the tool
                tool = next((t for t in all_tools if t.name == tool_name), None)
                
                if tool:
                    try:
                        result = tool.invoke(tool_args)
                        tool_outputs.append(
                            ToolMessage(
                                content=str(result),
                                tool_call_id=tool_call['id']
                            )
                        )
                        print(f"     ✅ {str(result)[:100]}")
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        tool_outputs.append(
                            ToolMessage(
                                content=error_msg,
                                tool_call_id=tool_call['id']
                            )
                        )
                        print(f"     ❌ {error_msg}")
        
        return {"messages": tool_outputs}
    
    # Router
    def should_continue(state: AgentState) -> Literal["tools", "end"]:
        """Determine if we should continue or end."""
        last_message = state['messages'][-1]
        
        if isinstance(last_message, AIMessage):
            content = last_message.content
            # Check if there are tool calls in the response
            if any(tool in content.lower() for tool in ['write_file', 'read_file', 'ls()', 'edit_file']):
                return "tools"
        
        return "end"
    
    # Build graph
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tools_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {"tools": "tools", "end": END}
    )
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()


def parse_tool_calls(text: str) -> list:
    """
    Parse tool calls from agent's response.
    Handles multiple formats.
    """
    tool_calls = []
    
    # Pattern 1: write_file("filename", "content")
    write_pattern = r'write_file\(\s*["\']([^"\']+)["\']\s*,\s*["\'](.+?)["\']\s*\)'
    for match in re.finditer(write_pattern, text, re.DOTALL):
        tool_calls.append({
            'name': 'write_file',
            'args': {'filename': match.group(1), 'content': match.group(2)},
            'id': f'call_{len(tool_calls)}'
        })
    
    # Pattern 2: read_file("filename")
    read_pattern = r'read_file\(\s*["\']([^"\']+)["\']\s*\)'
    for match in re.finditer(read_pattern, text):
        tool_calls.append({
            'name': 'read_file',
            'args': {'filename': match.group(1)},
            'id': f'call_{len(tool_calls)}'
        })
    
    # Pattern 3: edit_file("filename", "content")
    edit_pattern = r'edit_file\(\s*["\']([^"\']+)["\']\s*,\s*["\'](.+?)["\']\s*\)'
    for match in re.finditer(edit_pattern, text, re.DOTALL):
        tool_calls.append({
            'name': 'edit_file',
            'args': {'filename': match.group(1), 'new_content': match.group(2)},
            'id': f'call_{len(tool_calls)}'
        })
    
    # Pattern 4: ls()
    if 'ls()' in text:
        tool_calls.append({
            'name': 'ls',
            'args': {},
            'id': f'call_{len(tool_calls)}'
        })
    
    return tool_calls


def run_agent(graph, user_input: str, state: AgentState = None) -> AgentState:
    """
    Run the agent with a user input.
    """
    if state is None:
        state = AgentState(
            messages=[],
            files={},
            intermediate_steps=[]
        )
    
    # Add user message
    state['messages'].append(HumanMessage(content=user_input))
    
    # Run the graph with higher recursion limit for complex tasks
    try:
        final_state = graph.invoke(state, {"recursion_limit": 100})
        return final_state
    except Exception as e:
        print(f"Error running agent: {e}")
        raise