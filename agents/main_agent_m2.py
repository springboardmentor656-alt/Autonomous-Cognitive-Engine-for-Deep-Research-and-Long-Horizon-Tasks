"""
Milestone 2: Agent with Virtual File System (Memory)
"""

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Literal


from config.settings import settings
from state.agent_state import AgentState, TodoItem
from tools.planning_tools import PLANNING_TOOLS
from tools.file_system_tools import FILE_SYSTEM_TOOLS
from agents.prompts import get_prompt
from agents.m2_executor import execute_todo

ALL_TOOLS = PLANNING_TOOLS + FILE_SYSTEM_TOOLS


def create_llm():
    return ChatGroq(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        groq_api_key=settings.GROQ_API_KEY
    )

def agent_node(state: AgentState) -> AgentState:
    llm = create_llm()
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    prompt = get_prompt(settings.PROMPT_STYLE, milestone=2)

    messages = [SystemMessage(content=prompt)]

    if state["iteration_count"] == 0:
        messages.append(HumanMessage(content=state["user_request"]))
    else:
        messages.extend(state["messages"])

    if state["files"]:
        for fname, content in state["files"].items():
            messages.append(
                HumanMessage(content=f"[File: {fname}]\n{content[:1500]}")
            )

    response = llm_with_tools.invoke(messages)

    print(f"\n[DEBUG M2] Iteration {state['iteration_count'] + 1}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tc in response.tool_calls:
            print(f"[DEBUG M2] Tool: {tc['name']}")

    return {
        "messages": [response],
        "iteration_count": state["iteration_count"] + 1
    }


def tool_node_wrapper(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]

    if not (hasattr(last_message, "tool_calls") and last_message.tool_calls):
        return {"messages": []}

    tool_node = ToolNode(ALL_TOOLS)
    result = tool_node.invoke(state)

    updates = {"messages": result["messages"]}

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        args = tool_call["args"]

        print(f"[DEBUG M2] Processing tool: {tool_name}")

        if tool_name == "write_todos":
            tasks = args.get("tasks", [])
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
            updates["todos"] = todos
            print(f"[DEBUG M2] Created {len(todos)} tasks")

        elif tool_name == "write_file":
            filename = args.get("filename", "")
            content = args.get("content", "")
            if filename and content:
                files = state["files"].copy()
                files[filename] = content
                updates["files"] = files
                print(f"[DEBUG M2] Saved file: {filename}")

        elif tool_name == "edit_file":
            filename = args.get("filename", "")
            content = args.get("content", "")
            if filename and content:
                files = state["files"].copy()
                files[filename] = content
                updates["files"] = files
                print(f"[DEBUG M2] Updated file: {filename}")

        elif tool_name == "read_file":
            filename = args.get("filename", "")
            if filename in state["files"]:
                print(f"[DEBUG M2] Read file: {filename}")
            else:
                print(f"[DEBUG M2] File not found: {filename}")

        elif tool_name == "ls":
            print(f"[DEBUG M2] Files: {list(state['files'].keys())}")

    return updates


def should_continue(state: AgentState) -> Literal["tools", "execute", "final", "end"]:


    if state["iteration_count"] >= state["max_iterations"]:
        print("[DEBUG M2] Max iterations reached")
        return "final" if state["files"] else "end"


    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"


    if state["todos"] and any(t["status"] == "pending" for t in state["todos"]):
        print("[DEBUG M2] Executing pending TODO")
        return "execute"


    if state["files"]:
        print("[DEBUG M2] Creating final summary")
        return "final"

    return "end"


def create_milestone2_graph():
    workflow = StateGraph(AgentState)


    workflow.add_node("agent", agent_node)        
    workflow.add_node("tools", tool_node_wrapper)  
    workflow.add_node("executor", execute_todo)    
    workflow.add_node("final", final_summary)      

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "execute": "executor",
            "final": "final",
            "end": END
        }
    )

    workflow.add_edge("tools", "agent")

    workflow.add_edge("executor", "agent")

    return workflow.compile()


def final_summary(state):
    summary_prompt = f"""
Combine all the following files into a final financial plan:

{state["files"]}
"""

    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        groq_api_key=settings.GROQ_API_KEY
    )

    response = llm.invoke(summary_prompt)

    return {"final_output": response.content}


financial_agent_m2 = create_milestone2_graph()
