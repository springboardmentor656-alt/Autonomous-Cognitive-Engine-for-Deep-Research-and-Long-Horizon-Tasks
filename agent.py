from langgraph.graph import StateGraph
from state import AgentState
from tools import delegate_task

def planner(state: AgentState):
    todos = [
        "Understand AI basics",
        "Learn Machine Learning concepts",
        "Summarize required skills for AI/ML jobs",
        "Plan career roadmap"
    ]
    return {"todos": todos}


def executor(state: AgentState):
    delegated_results = {}

    for todo in state["todos"]:
        if "Summarize" in todo:
            result = delegate_task.invoke({
                "agent_name": "summarizer",
                "task_input": todo
            })
            delegated_results[todo] = result

    return {"delegated_results": delegated_results}


def build_main_agent():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner)
    graph.add_node("executor", executor)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")

    return graph.compile()


app = build_main_agent()
