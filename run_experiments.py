from dotenv import load_dotenv
load_dotenv()

from main import graph


def run_demo():
    initial_state = {
        "messages": [
            "Summarize the following article: <long text here>..."
        ],
        "todos": [],
        "files": {},
        "sub_agent_results": [],   # required by orchestrator
        "done": False
    }

    final = graph.invoke(initial_state)

    print("Files:", final.get("files", {}))
    print("Messages:", final.get("messages", []))


if __name__ == "__main__":
    run_demo()
