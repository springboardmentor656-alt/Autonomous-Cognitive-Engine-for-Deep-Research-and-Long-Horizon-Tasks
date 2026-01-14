from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import Literal

from config.settings import settings
from state.agent_state import AgentState, TodoItem
from tools.planning_tools import PLANNING_TOOLS
from agents.prompts import get_prompt

def create_llm():
    """Create LLM instance with Groq"""
    return ChatGroq(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        groq_api_key=settings.GROQ_API_KEY
    )

def agent_node(state: AgentState) -> AgentState:
    """
    Main agent reasoning node.
    The LLM decides what to do next based on current state.
    """
    llm = create_llm()
    llm_with_tools = llm.bind_tools(PLANNING_TOOLS)
    
    prompt = get_prompt(settings.PROMPT_STYLE)
    
    messages = []
    
    messages.append(SystemMessage(content=prompt))
    
    if state["iteration_count"] == 0:
        messages.append(HumanMessage(content=state["user_request"]))
    else:
        messages.extend(state["messages"])
    
    if state["todos"]:
        summary = f"\n\nCurrent status: Created {len(state['todos'])} tasks. Task planning is complete."
        messages.append(HumanMessage(content=summary))
    
    response = llm_with_tools.invoke(messages)
    
    print(f"\n[DEBUG] Iteration {state['iteration_count'] + 1}")
    print(f"[DEBUG] Has tool calls: {hasattr(response, 'tool_calls') and bool(response.tool_calls)}")
    if hasattr(response, 'tool_calls') and response.tool_calls:
        print(f"[DEBUG] Tool called: {response.tool_calls[0]['name']}")
    
    return {
        "messages": [response],
        "iteration_count": state["iteration_count"] + 1
    }

def tool_node_wrapper(state: AgentState) -> AgentState:
    """
    Execute tools and update state based on tool results.
    This is where we actually modify the todos list.
    """
    last_message = state["messages"][-1]
    
    if not (hasattr(last_message, "tool_calls") and last_message.tool_calls):
        print("[DEBUG] No tool calls in message")
        return {"messages": []}
    
    print(f"[DEBUG] Processing {len(last_message.tool_calls)} tool call(s)")
    
    try:
        tool_node = ToolNode(PLANNING_TOOLS)
        result = tool_node.invoke(state)
        print("[DEBUG] Tool execution successful")
    except Exception as e:
        print(f"[DEBUG] Tool execution error: {e}")
        from langchain_core.messages import ToolMessage
        error_msg = ToolMessage(
            content=f"Error executing tool: {str(e)}",
            tool_call_id=last_message.tool_calls[0]["id"]
        )
        return {"messages": [error_msg]}
    
    for tool_call in last_message.tool_calls:
        print(f"[DEBUG] Tool call: {tool_call['name']}")
        print(f"[DEBUG] Tool args: {tool_call['args']}")
        
        if tool_call["name"] == "write_todos":
            args = tool_call["args"]
            
            if "tasks" in args:
                tasks = args["tasks"]
            elif isinstance(args, list):
                tasks = args
            else:
                print(f"[DEBUG] Unexpected args format: {args}")
                continue
            
            todos = [
                TodoItem(
                    id=i,
                    description=task,
                    status="pending",
                    result=None,
                    assigned_to="main"
                )
                for i, task in enumerate(tasks)
            ]
            
            print(f"[DEBUG] Created {len(todos)} TODO items")
            for i, todo in enumerate(todos):
                print(f"[DEBUG]   {i+1}. {todo['description'][:60]}...")
            
            return {
                "messages": result["messages"],
                "todos": todos
            }
    
    return {"messages": result["messages"]}

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """
    Decide whether to continue or end.
    """
    if state["iteration_count"] >= state["max_iterations"]:
        print(f"[DEBUG] Max iterations reached ({state['max_iterations']})")
        return "end"
    
    if state["todos"]:
        print(f"[DEBUG] TODOs exist, ending")
        return "end"
    
    last_message = state["messages"][-1]
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print(f"[DEBUG] Routing to tools")
        return "tools"
    
    print(f"[DEBUG] No tool calls, continuing to agent")
    return "end"

def create_milestone1_graph():
    """
    Create the LangGraph workflow for Milestone 1.
    Focus: Task planning with write_todos tool.
    """
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node_wrapper)
    
    workflow.set_entry_point("agent")
    
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()

financial_agent = create_milestone1_graph()