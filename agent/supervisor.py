from tools.planning import write_todos
from agent.vfs import write_file, read_file, ls
from agent.delegation import delegate_task
from langsmith import traceable


@traceable(name="Task Supervisor")
def run_tasks(tasks):
    for idx, task in enumerate(tasks, start=1):
        print("\n" + "=" * 40)
        print(f"Task {idx}: {task}")
        print("=" * 40)

        # 1️⃣ Planning Phase
        todos = write_todos(task)
        todos_file = f"task_{idx}_todos.txt"
        write_file(todos_file, "\n".join(todos))

        delegated_results = []

        # OPTIONAL: example article content
        article_content = """
Artificial Intelligence is transforming industries such as healthcare,
finance, and education. It enables automation, improves decision-making,
and increases efficiency through data-driven insights.
"""

        # 2️⃣ Delegation Phase
        SUMMARY_KEYWORDS = ["summarize", "summary", "overview", "analyze"]

        for todo in todos:
            if any(word in todo.lower() for word in SUMMARY_KEYWORDS):
                enriched_task = f"""
{todo}

Content to summarize:
{article_content}
"""
                result = delegate_task(
                    agent_name="summarizer",
                    task=enriched_task
                )
                delegated_results.append(f"[Summarization Result]\n{result}")
            else:
                delegated_results.append(todo)

        # 3️⃣ Integration Phase
        final_output = f"""Task:
{task}

Subtasks & Results:
{chr(10).join(delegated_results)}

Summary:
The supervisor planned the task, delegated summarization
to a specialized sub-agent, and integrated the results.
"""

        final_file = f"task_{idx}_final.txt"
        write_file(final_file, final_output)

        # 4️⃣ Debug + Trace Visibility
        print("Files in VFS:", ls())
        print("\nFinal Output:\n")
        print(read_file(final_file))
