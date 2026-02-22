from planner import write_todos
from tools.delegate_task import delegate_task

def build_deep_agent(user_task: str):
    todos = write_todos(user_task)
    results = []

    for todo in todos:
        if "Summarize" in todo or "Research" in todo:
            result = delegate_task(todo)
            results.append(result)
        else:
            results.append(f"Handled internally: {todo}")

    return results
