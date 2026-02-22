import time
from datetime import datetime
from subagents.judge import run as judge_run

from langgraph.graph import StateGraph, END
from langsmith import traceable
from langchain_groq import ChatGroq

from agent.state import AgentState
from tools.planning import write_todos
from agent.delegation import delegate_task
from agent.vfs import write_file, ls


# =====================================
# LLM for routing decisions (optional future expansion)
# =====================================
router_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


# =====================================
# PLANNER NODE
# =====================================
@traceable(name="Planner Node")
def planner_node(state: AgentState):

    todos = write_todos(state["task"])

    return {
        "todos": todos,
        "current_index": 0,
        "delegated_results": [],
        "current_todo": None,
        "next_step": None,
        "final_output": ""
    }


# =====================================
# ORCHESTRATOR NODE (CORE BRAIN - FIXED)
# =====================================
@traceable(name="Orchestrator Node")
def orchestrator_node(state: AgentState):

    total_todos = len(state["todos"])
    current_index = state["current_index"]
    has_final_output = bool(state["final_output"])

    # 1️⃣ If still have research left → continue researching
    if current_index < total_todos:
        return {
            "current_todo": state["todos"][current_index],
            "next_step": "researcher"
        }

    # 2️⃣ If all research done but no final report → summarize
    if current_index >= total_todos and not has_final_output:
        return {
            "next_step": "summarizer"
        }

    # 3️⃣ If summary exists → finalize
    return {
        "next_step": "finalize"
    }


# =====================================
# RESEARCH NODE
# =====================================
@traceable(name="Research Node")
def research_node(state: AgentState):

    todo = state["current_todo"]

    result = delegate_task("researcher", todo)

    formatted_result = f"[Research Output]\n{result}"

    return {
        "delegated_results": state["delegated_results"] + [formatted_result],
        "current_index": state["current_index"] + 1
    }


# =====================================
# SUMMARIZER NODE
# =====================================
@traceable(name="Summarizer Node")
def summarize_node(state: AgentState):

    combined_research = "\n\n".join(state["delegated_results"])

    summary = delegate_task(
        "summarizer",
        state["task"],
        combined_research
    )

    return {
        "final_output": summary
    }


# =====================================
# FINAL NODE
# =====================================
@traceable(name="Final Integration Node")
def final_node(state: AgentState):

    formatted_output = f"""
# AI Multi-Agent Cognitive Execution Report

## Original Task
{state['task']}

---

## Planned Subtasks
{chr(10).join(f"- {todo}" for todo in state['todos'])}

---

## Final Report
{state['final_output']}
"""

    # 🔥 Save as Markdown file (Task 3 requirement)
    write_file("final_report.md", formatted_output)

    return {
        "final_output": formatted_output
    }


# =====================================
# BUILD GRAPH
# =====================================
def build_graph():

    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("research", research_node)
    workflow.add_node("summarize", summarize_node)
    workflow.add_node("final", final_node)

    workflow.set_entry_point("planner")

    workflow.add_edge("planner", "orchestrator")

    workflow.add_conditional_edges(
        "orchestrator",
        lambda state: state["next_step"],
        {
            "researcher": "research",
            "summarizer": "summarize",
            "finalize": "final"
        }
    )

    workflow.add_edge("research", "orchestrator")
    workflow.add_edge("summarize", "orchestrator")
    workflow.add_edge("final", END)

    return workflow.compile()

# =====================================
# TASK EXECUTION
# =====================================
@traceable(name="Task Supervisor")
def run_tasks(task: str):

    app = build_graph()

    start_time = time.time()

    initial_state = {
        "task": task,
        "todos": [],
        "current_index": 0,
        "delegated_results": [],
        "current_todo": None,
        "next_step": None,
        "final_output": "",
        "evaluation": "",
        "execution_time": 0.0
    }

    # Run graph
    result = app.invoke(initial_state)

    end_time = time.time()
    execution_time = round(end_time - start_time, 2)

    final_output = result.get("final_output", "")

    # 🔎 Run evaluation (if you have judge_run)
    evaluation_result = judge_run(task, final_output)
    evaluation_text = evaluation_result.get("evaluation", "")

    # ============================
    # CREATE MARKDOWN REPORT
    # ============================

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"final_report_{timestamp}.md"

    markdown_content = f"""
# AI Autonomous Cognitive Engine Report

## Task
{task}

---

## Final Output
{final_output}

---

## Evaluation
{evaluation_text}

---

## Execution Metrics
- Execution Time: {execution_time} seconds
- Subtasks Generated: {len(result.get("todos", []))}
- Output Length: {len(final_output)} characters
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"\nReport saved as: {filename}")

    # ============================
    # RETURN FOR LANGSMITH
    # ============================

    return {
        "output": final_output
    }