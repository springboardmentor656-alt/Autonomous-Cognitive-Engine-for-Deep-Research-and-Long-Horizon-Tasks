def default_state(task: str):
    return {
        "task": task,
        "messages": [],
        "todos": [],
        "current_index": 0,
        "files": {},
        "sub_agent_results": [],
        "final_report": ""
    }
