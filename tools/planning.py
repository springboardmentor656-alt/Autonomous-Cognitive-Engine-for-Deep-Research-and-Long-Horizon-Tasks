def write_todos(task: str):
    """
    Breaks a complex task into smaller TODO items.
    """
    todos = []

    if "research" in task.lower():
        todos = [
            "Understand the topic",
            "Search for reliable sources",
            "Summarize collected information",
            "Prepare final report"
        ]
    else:
        todos = [
            "Understand the requirement",
            "Break task into steps",
            "Execute each step",
            "Review final output"
        ]

    return todos
