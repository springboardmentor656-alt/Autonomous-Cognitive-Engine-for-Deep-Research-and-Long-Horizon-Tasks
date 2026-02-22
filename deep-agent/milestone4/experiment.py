from agent.graph import app
from langchain_core.messages import HumanMessage

def run_single_experiment(task: str):

    initial_state = {
        "messages": [HumanMessage(content=task)],
        "todos": [],
        "files": {},
        "sub_agent_results": {},
        "current_task": None,
        "final_report_path": None
    }

    result = app.invoke(initial_state)

    report = result["files"][result["final_report_path"]]

    return report


if __name__ == "__main__":
    report = run_single_experiment(
        "Write a research report on green hydrogen"
    )
    print(report)
