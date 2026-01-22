"""
Milestone 3: Supervisor Agent with Sub-Agent Delegation

This agent can:
1. Create task plans (M1)
2. Use file system (M2)
3. Delegate to specialists (M3)
"""

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from typing import Literal

from config.settings import settings
import state
from state.agent_state import AgentState, TodoItem
from tools.planning_tools import PLANNING_TOOLS
from tools.file_system_tools import FILE_SYSTEM_TOOLS
from tools.delegation_tools import DELEGATION_TOOLS
from agents.sub_agents import delegate_to_specialist

ALL_SUPERVISOR_TOOLS = PLANNING_TOOLS + FILE_SYSTEM_TOOLS + DELEGATION_TOOLS

SUPERVISOR_PROMPT = """You are a Financial Planning Supervisor Agent.

# YOUR ROLE

You coordinate complex financial planning tasks by:
1. Breaking down requests into sub-tasks
2. Delegating specialized work to expert sub-agents
3. Synthesizing results into comprehensive plans

# YOUR TEAM

You have access to specialist sub-agents:

- **debt_specialist**: Expert in debt analysis, payoff strategies, interest optimization
- **budget_analyst**: Expert in budget creation, expense analysis, cash flow
- **investment_advisor**: Expert in retirement planning, portfolio allocation (coming soon)
- **tax_optimizer**: Expert in tax strategies, deductions (coming soon)

# YOUR TOOLS

## Planning
- write_todos: Create task breakdown

## Delegation (NEW!)
- delegate_task: Send tasks to specialists

## File System
- write_file, read_file, edit_file, ls: Manage context

# WORKFLOW

When you receive a request:

1. Plan: Use write_todos to break it down into detailed, outcome-focused tasks.

Each task should:
- Be specific to the financial domain
- Include what analysis is needed
- Mention expected outputs (calculations, strategies, timelines)
- Be suitable for delegation to specialists

2. **Identify**: Which tasks need specialists?
   - Debt calculations → debt_specialist
   - Budget creation → budget_analyst
   - Investment advice → investment_advisor
   - Tax strategies → tax_optimizer
3. **Delegate**: Use delegate_task for specialist work
4. **Save**: Use write_file to store specialist results
5. **Synthesize**: Combine all results into final plan

# EXAMPLE (HIGH QUALITY)

User: "I have $10k in credit card debt and want to pay it off"

Your workflow:

1. write_todos([
   "Analyze each credit card’s APR, minimum payment, and interest cost over time",
   "Determine whether avalanche or snowball method minimizes total interest",
   "Calculate exact monthly payment allocation using $800/month budget",
   "Create a 12–18 month payoff timeline with milestones"
])

2. delegate_task(
   "Analyze $10k credit card debt with APRs 22%, 19%, 15% and recommend the best payoff strategy with detailed calculations",
   "debt_specialist"
)

3. write_file("credit_card_debt_plan.txt", specialist_response.content)

4. Synthesize results into a clear payoff plan


ALWAYS delegate complex domain-specific tasks to specialists!
"""

def create_llm():
    """Create LLM instance"""
    return ChatGroq(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        groq_api_key=settings.GROQ_API_KEY
    )

def supervisor_node(state: AgentState) -> AgentState:
    """Supervisor reasoning node"""
    llm = create_llm()
    llm_with_tools = llm.bind_tools(ALL_SUPERVISOR_TOOLS)
    
    messages = [SystemMessage(content=SUPERVISOR_PROMPT)]
    
    if state["iteration_count"] == 0:
        messages.append(HumanMessage(content=state["user_request"]))
    else:
        messages.extend(state["messages"])
    
    if state["files"]:
        file_summary = f"Files available: {', '.join(state['files'].keys())}"
        messages.append(HumanMessage(content=f"[Context: {file_summary}]"))
    
    response = llm_with_tools.invoke(messages)
    
    print(f"\n[SUPERVISOR] Iteration {state['iteration_count'] + 1}")
    if hasattr(response, 'tool_calls') and response.tool_calls:
        for tc in response.tool_calls:
            print(f"[SUPERVISOR] Planning to use: {tc['name']}")
    
    return {
        "messages": [response],
        "iteration_count": state["iteration_count"] + 1
    }

def tool_execution_node(state: AgentState) -> AgentState:
    """Execute tools including delegation"""
    last_message = state["messages"][-1]
    
    if not (hasattr(last_message, "tool_calls") and last_message.tool_calls):
        return {"messages": []}
    
    updates = {"messages": []}
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        args = tool_call["args"]
        tool_call_id = tool_call["id"]
        
        print(f"\n[TOOL EXECUTION] {tool_name}")
        
        if tool_name == "delegate_task":
            specialist = args.get("specialist", "")
            task_desc = args.get("task_description", "")
            
            try:
                result = delegate_to_specialist(specialist, task_desc)
                
                tool_response = ToolMessage(
                    content=result,
                    tool_call_id=tool_call_id
                )
                updates["messages"].append(tool_response)
                
                count = len([f for f in state["files"] if specialist in f]) + 1
                filename = f"{specialist}_{count}_result.txt"
                files = state["files"].copy()
                files[filename] = result
                updates["files"] = files
                
                print(f"[TOOL EXECUTION] Delegation complete, saved to {filename}")
                
            except Exception as e:
                error_msg = ToolMessage(
                    content=f"Delegation error: {str(e)}",
                    tool_call_id=tool_call_id
                )
                updates["messages"].append(error_msg)
                print(f"[TOOL EXECUTION] Delegation failed: {e}")
        
        else:
            tool_node = ToolNode(ALL_SUPERVISOR_TOOLS)
            result = tool_node.invoke(state)
            
            if tool_name == "write_todos":
                tasks = args.get("tasks", [])
                todos = [
                    TodoItem(
                        id=i,
                        description=task,
                        status="pending",
                        result=None,
                        assigned_to="supervisor"
                    )
                    for i, task in enumerate(tasks)
                ]
                updates["todos"] = todos
                print(f"[TOOL EXECUTION] Created {len(todos)} tasks")
            
            elif tool_name == "write_file":
                filename = args.get("filename", "")
                content = args.get("content", "")
                if filename and content:
                    files = state["files"].copy()
                    files[filename] = content
                    updates["files"] = files
                    print(f"[TOOL EXECUTION] Saved {filename}")
            
            elif tool_name == "edit_file":
                filename = args.get("filename", "")
                content = args.get("content", "")
                if filename and content:
                    files = state["files"].copy()
                    files[filename] = content
                    updates["files"] = files
                    print(f"[TOOL EXECUTION] Updated {filename}")
            
            updates["messages"].extend(result.get("messages", []))
    
    return updates

def should_continue(state: AgentState) -> Literal["tools", "final", "end"]:

    if state["iteration_count"] >= state["max_iterations"]:
        return "final" if state["files"] else "end"

    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    has_plan = len(state["todos"]) >= 3
    has_delegated = any("_result.txt" in fname for fname in state["files"].keys())

    if has_plan and has_delegated:
        return "final"

    return "end"


def create_supervisor_agent():
    workflow = StateGraph(AgentState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("tools", tool_execution_node)
    workflow.add_node("final", final_summary)

    workflow.set_entry_point("supervisor")

    workflow.add_conditional_edges(
        "supervisor",
        should_continue,
        {
            "tools": "tools",
            "final": "final",
            "end": END
        }
    )

    workflow.add_edge("tools", "supervisor")
    workflow.add_edge("final", END)

    return workflow.compile()

def final_summary(state):
    summary_prompt = "You are a Financial Planning Expert.\n\n"
    summary_prompt += "Using the following specialist reports:\n\n"

    for fname, content in state["files"].items():
        summary_prompt += f"\n--- {fname} ---\n{content}\n"

    summary_prompt += """
Create a clear, professional financial plan with:

1. Best payoff strategy
2. Monthly payment breakdown
3. Timeline
4. Budget recommendations
5. Long-term advice

Write in a structured, readable format.
"""

    llm = create_llm()
    response = llm.invoke(summary_prompt)

    return {
        "final_output": response.content,
        "messages": [response]
    }



supervisor_agent = create_supervisor_agent()