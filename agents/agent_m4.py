from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from typing import Literal
import uuid

from config.settings import settings
from state.agent_state import AgentState, TodoItem
from tools.planning_tools import PLANNING_TOOLS
from tools.file_system_tools import FILE_SYSTEM_TOOLS
from tools.delegation_tools import DELEGATION_TOOLS
from agents.sub_agents import delegate_to_specialist

ALL_TOOLS_M4 = PLANNING_TOOLS + FILE_SYSTEM_TOOLS + DELEGATION_TOOLS

FINAL_AGENT_PROMPT = """You are an autonomous Advanced Financial Planning Agent capable of handling complex, multi-step financial scenarios using planning, memory, and specialist delegation.

CAPABILITIES

Planning:
- Break complex requests into structured tasks using write_todos

Memory:
- Persist and retrieve data using write_file, read_file, edit_file, ls

Delegation:
- Delegate domain-specific tasks using delegate_task

Specialist Team:
- debt_specialist → debt analysis, payoff strategies, consolidation
- budget_analyst → budgeting, expense optimization, cash flow
- investment_advisor → retirement planning, portfolio allocation
- tax_optimizer → tax strategies (when applicable)

EXECUTION FRAMEWORK

1. Analyze
Identify:
- Financial domains involved (debt, budget, investment, tax, emergency, insurance)
- Required calculations
- Missing information

2. Plan
Create structured task list with write_todos.
Order logically: gather → analyze → recommend → synthesize.

3. Execute & Delegate
- Delegate domain tasks to specialists.
- Only delegate if relevant domain exists. like, If no debt → do NOT call debt_specialist.
- Immediately save every specialist result using write_file.
- Use descriptive filenames (e.g., debt_analysis.txt, budget_plan.txt).

Always delegate:
- Debt calculations → debt_specialist
- Budget creation → budget_analyst
- Retirement/portfolio planning → investment_advisor
- Tax optimization → tax_optimizer


Handle internally:
- Initial scoping
- Cross-domain synthesis
- Final report generation
- Simple arithmetic

4. Synthesize
- Read all saved files.
- Resolve gaps or conflicts.
- Create unified financial plan.

5. DELIVER a DETAILED FINANCIAL MASTER PLAN (MANDATORY)

FINAL OUTPUT FORMAT (STRICT):
The final plan MUST:
1. Current Financial Snapshot
2. Debt Strategy (with timeline in months)
3. Monthly Allocation Table (numbers required)
4. Emergency Fund Target (calculation shown)
5. Investment Strategy (allocation %)
6. 3-Phase Roadmap (0-12m, 1-3y, 3-5y)

Generate one structured financial master plan between 550–700 words.
Call write_file exactly once with filename "final_financial_plan.txt".
Do NOT call write_file more than once.
Do NOT rewrite the final plan.

Only generate the final comprehensive plan ONCE.
Do not rewrite it multiple times.

Handle the user request autonomously and systematically.
"""

def create_llm():
    return ChatGroq(
        model=settings.LLM_MODEL,
        temperature=0,
        groq_api_key=settings.GROQ_API_KEY
    )

def agent_node(state: AgentState) -> AgentState:
    llm = create_llm()
    llm_with_tools = llm.bind_tools(ALL_TOOLS_M4)
    
    messages = [SystemMessage(content=FINAL_AGENT_PROMPT)]
    
    if state["iteration_count"] == 0:
        messages.append(HumanMessage(content=state["user_request"]))
    else:
        messages.extend(state["messages"])
    
    context_info = []
    
    if state["todos"]:
        completed = sum(1 for t in state["todos"] if t["status"] == "completed")
        context_info.append(f"Progress: {completed}/{len(state['todos'])} tasks completed")
    
    if state["files"]:
        context_info.append(f"Files: {', '.join(state['files'].keys())}")
    
    if context_info:
        messages.append(HumanMessage(content=f"[Status: {' | '.join(context_info)}]"))
    
    response = llm_with_tools.invoke(messages)
    
    print(f"\n[M4 AGENT] Iteration {state['iteration_count'] + 1}/{state['max_iterations']}")
    if hasattr(response, 'tool_calls') and response.tool_calls:
        for tc in response.tool_calls:
            print(f"[M4 AGENT] → {tc['name']}")
    else:
        print(f"[M4 AGENT] → Generating response (no tools)")
    
    return {
        "messages": [response],
        "iteration_count": state["iteration_count"] + 1
    }

def tool_execution_node(state: AgentState) -> AgentState:
    """Execute all tools including delegation"""
    last_message = state["messages"][-1]
    
    if not (hasattr(last_message, "tool_calls") and last_message.tool_calls):
        return {"messages": []}
    
    updates = {"messages": [], "todos": state["todos"], "files": state["files"].copy()}
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        args = tool_call["args"]
        tool_call_id = tool_call["id"]
        
        if tool_name == "delegate_task":
            specialist = args.get("specialist", "")
            task_desc = args.get("task_description", "")

            existing = any(
                specialist in f and f.endswith("_result.txt")
                for f in state["files"].keys()
            )
            if existing:
                print(f"[M4 DELEGATION] Skipping duplicate delegation to {specialist}")
                continue

            try:
                print(f"\n[M4 DELEGATION] Delegating to {specialist}...")
                result = delegate_to_specialist(specialist, task_desc)

                filename = f"{specialist}_{tool_call_id}_result.txt"
                updates["files"][filename] = result

                tool_response = ToolMessage(
                    content=result,
                    tool_call_id=tool_call_id
                )
                updates["messages"].append(tool_response)

                print(f"[M4 DELEGATION] Saved to {filename}")

            except Exception as e:
                error_msg = ToolMessage(
                    content=f"Delegation error: {str(e)}",
                    tool_call_id=tool_call_id
                )
                updates["messages"].append(error_msg)
                print(f"[M4 DELEGATION] Error: {e}")

        
        else:
            tool_node = ToolNode(ALL_TOOLS_M4)
            result = tool_node.invoke(state)
            
            if tool_name == "write_todos":
                tasks = args.get("tasks", [])
                updates["todos"] = [
                    TodoItem(
                        id=i,
                        description=task,
                        status="pending",
                        result=None,
                        assigned_to="agent"
                    )
                    for i, task in enumerate(tasks)
                ]
                print(f"[M4 PLANNING] Created {len(tasks)} tasks")
            
            elif tool_name == "write_file":
                filename = args.get("filename", "")
                content = args.get("content", "")

                if not filename or not content:
                    continue

                # Force all final-like names into ONE canonical filename
                if any(keyword in filename.lower() for keyword in [
                    "final",
                    "comprehensive",
                    "financial_plan",
                    "report",
                    "master_plan"
                ]):
                    filename = "final_financial_plan.txt"

                    # Prevent overwriting the final plan
                    if filename in updates["files"]:
                        print("[M4 FILE] Final plan already exists → Skipping rewrite")
                        continue

                    updates["files"][filename] = content
                    print(f"[M4 FILE] Saved final_financial_plan.txt ({len(content)} chars)")

                else:
                    updates["files"][filename] = content
                    print(f"[M4 FILE] Saved {filename} ({len(content)} chars)")

            
            elif tool_name == "edit_file":
                filename = args.get("filename", "")
                content = args.get("content", "")
                if filename and content:
                    updates["files"][filename] = content
                    print(f"[M4 FILE] Updated {filename}")
            
            elif tool_name == "update_todo_status":
                todo_id_raw = args.get("todo_id", -1)
                status = args.get("status", "")

                try:
                    todo_id = int(todo_id_raw)
                except (ValueError, TypeError):
                    print(f"[M4 ERROR] Invalid todo_id: {todo_id_raw}")
                    continue

                if 0 <= todo_id < len(updates["todos"]):
                    updates["todos"][todo_id]["status"] = status
                    print(f"[M4 PLANNING] Task {todo_id} → {status}")
                else:
                    print(f"[M4 ERROR] todo_id out of range: {todo_id}")            
            updates["messages"].extend(result.get("messages", []))
    
    return updates

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    if state["iteration_count"] >= state["max_iterations"]:
        print("[M4 ROUTING] Max iterations reached → END")
        return "end"

    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print("[M4 ROUTING] Tool call detected → TOOLS")
        return "tools"

    if "final_financial_plan.txt" in state["files"]:
        print("[M4 ROUTING] Final plan detected → END")
        return "end"

    return "end"


def create_final_agent():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_execution_node)
    
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

agent_m4 = create_final_agent()