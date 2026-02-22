from agent.graph import app
from langchain_core.messages import HumanMessage

if __name__ == "__main__":

    initial_state = {
        "messages": [HumanMessage(
            content="Summarize renewable energy trends and combine findings"
        )],
        "todos": [],
        "files": {},
        "sub_agent_results": {},
        "current_task": None,
        "final_report_path": None
    }

    result = app.invoke(initial_state)

    print("Stored files:")
    print(result["files"].keys())
