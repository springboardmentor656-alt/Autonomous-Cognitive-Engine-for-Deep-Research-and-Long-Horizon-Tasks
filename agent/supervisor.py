import os
from typing import TypedDict, List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from langsmith import traceable
from langgraph.graph import StateGraph, END
from tools.planning import write_todos
from tools.delegation import delegate_task, list_subagents

load_dotenv()

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)


class SupervisorState(TypedDict):
    input: str
    todos: List[str]
    completed_todos: List[str]
    current_todo_index: int
    status: str
    files: Dict[str, str]
    final_output: str
    error: str


def _build_prior_context(state: SupervisorState, current_idx: int) -> str:
    previous = []
    for i in range(current_idx):
        prev_file = f"todo_{i + 1}_result.txt"
        if prev_file in state["files"]:
            previous.append(f"Step {i + 1}: {state['files'][prev_file][:300]}...")
    return "\n\nContext:\n" + "\n".join(previous) if previous else ""


def decide_delegation(todo_item: str, registry: dict, context: str) -> dict:
    lowered = todo_item.lower()
    task_input = f"{todo_item}{context}" if context else todo_item

    if any(word in lowered for word in ["search", "web", "latest", "current", "news", "source"]):
        if "web_search_agent" in registry:
            return {"delegate_to": "web_search_agent", "task_input": task_input}

    if "summarize" in lowered or "summary" in lowered:
        if "summarization_agent" in registry:
            return {"delegate_to": "summarization_agent", "task_input": task_input}

    if any(word in lowered for word in ["research", "investigate", "find", "explore", "compare"]):
        if "researcher_agent" in registry:
            return {"delegate_to": "researcher_agent", "task_input": task_input}

    return {"delegate_to": None, "task_input": task_input}


@traceable(name="planning_node")
def planning_node(state: SupervisorState) -> SupervisorState:
    try:
        todos = write_todos(state["input"])
        state["files"]["todos.txt"] = "\n".join(
            [f"{i + 1}. {todo}" for i, todo in enumerate(todos)]
        )
        return {
            **state,
            "todos": todos,
            "status": "planned",
            "current_todo_index": 0,
            "error": ""
        }
    except Exception as e:
        return {**state, "status": "error", "error": str(e)}


@traceable(name="execution_node")
def execution_node(state: SupervisorState) -> SupervisorState:
    current_idx = state["current_todo_index"]
    if current_idx >= len(state["todos"]):
        return {**state, "status": "executed"}

    todo_item = state["todos"][current_idx]
    todo_number = current_idx + 1

    try:
        context = _build_prior_context(state, current_idx)

        delegation = decide_delegation(todo_item, list_subagents(), context)
        if delegation["delegate_to"]:
            result = delegate_task(delegation["task_input"], delegation["delegate_to"])
        else:
            prompt = (
                "Execute the task clearly and concisely. "
                "Use bullets where helpful."
            )
            response = client.chat.completions.create(
                model="moonshotai/Kimi-K2-Thinking",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Task: {todo_item}{context}"}
                ],
                temperature=0.7,
                max_tokens=800
            )
            choice = response.choices[0] if response and getattr(response, "choices", None) else None
            content = choice.message.content if choice and getattr(choice, "message", None) else None
            result = content.strip() if content else "Model returned empty content."

        result_filename = f"todo_{todo_number}_result.txt"
        state["files"][result_filename] = result

        completed = state["completed_todos"].copy()
        completed.append(todo_item)

        return {
            **state,
            "completed_todos": completed,
            "current_todo_index": current_idx + 1,
            "error": ""
        }
    except Exception as e:
        return {**state, "status": "error", "error": str(e)}


def should_continue_execution(state: SupervisorState) -> str:
    if state.get("error"):
        return "synthesize"
    if state["current_todo_index"] >= len(state["todos"]):
        return "synthesize"
    return "execute"


@traceable(name="synthesis_node")
def synthesis_node(state: SupervisorState) -> SupervisorState:
    try:
        todos = state["todos"]
        all_results = []
        for i in range(len(state["completed_todos"])):
            result_file = f"todo_{i + 1}_result.txt"
            if result_file in state["files"]:
                result_content = state["files"][result_file]
                all_results.append(f"### Step {i + 1}: {todos[i]}\n{result_content}\n")

        summary = (
            "# EXECUTION SUMMARY\n\n"
            f"## Task\n{state['input']}\n\n"
            "## Status\n"
            f"- Total TODOs: {len(todos)}\n"
            f"- Completed: {len(state['completed_todos'])}\n"
            f"- Status: {'COMPLETE' if len(state['completed_todos']) == len(todos) else 'PARTIAL'}\n\n"
            "## Detailed Results\n\n"
            + "\n".join(all_results)
        )
        if state.get("error"):
            summary += f"\n\n## Errors Encountered\n{state['error']}\n"
        state["files"]["execution_summary.txt"] = summary

        synthesis_prompt = (
            "Synthesize the results into a clear final output. "
            "Use sections and bullets when helpful."
        )
        response = client.chat.completions.create(
            model="moonshotai/Kimi-K2-Thinking",
            messages=[
                {"role": "system", "content": synthesis_prompt},
                {"role": "user", "content": f"Task: {state['input']}\n\nResults:\n{chr(10).join(all_results)}"}
            ],
            temperature=0.5,
            max_tokens=1500
        )

        choice = response.choices[0] if response and getattr(response, "choices", None) else None
        content = choice.message.content if choice and getattr(choice, "message", None) else None
        final_output = content.strip() if content else summary

        state["files"]["final_output.txt"] = final_output

        return {**state, "final_output": final_output, "status": "complete"}
    except Exception as e:
        basic_summary = (
            f"Task: {state['input']}\n"
            f"Completed {len(state['completed_todos'])} of {len(state['todos'])} steps."
        )
        return {**state, "final_output": basic_summary, "status": "complete", "error": str(e)}


def build_supervisor_graph():
    workflow = StateGraph(SupervisorState)
    workflow.add_node("plan", planning_node)
    workflow.add_node("execute", execution_node)
    workflow.add_node("synthesize", synthesis_node)
    workflow.set_entry_point("plan")
    workflow.add_edge("plan", "execute")
    workflow.add_conditional_edges(
        "execute",
        should_continue_execution,
        {"execute": "execute", "synthesize": "synthesize"}
    )
    workflow.add_edge("synthesize", END)
    return workflow.compile()


supervisor_graph = build_supervisor_graph()


@traceable(name="supervisor_agent")
def supervisor_agent(user_input: str) -> SupervisorState:
    initial_state = SupervisorState(
        input=user_input,
        todos=[],
        completed_todos=[],
        current_todo_index=0,
        status="starting",
        files={},
        final_output="",
        error=""
    )

    return supervisor_graph.invoke(initial_state)
