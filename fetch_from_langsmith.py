from langsmith import Client

client = Client()

PROJECT_NAME = "milestone-1-final"


def load_memory():
    """
    Fetch runs from LangSmith and build a
    prompt -> todos mapping
    """
    memory = {}

    runs = client.list_runs(project_name=PROJECT_NAME)

    for run in runs:
        messages = run.inputs.get("messages")
        todos = run.outputs.get("todos")

        if not messages or not todos:
            continue

        # ✅ FIX: extract prompt as STRING
        prompt = messages[0]

        # Ensure key is hashable
        if isinstance(prompt, list):
            prompt = " ".join(prompt)

        memory[prompt] = todos

    return memory


if __name__ == "__main__":
    memory = load_memory()

    print("\n📋 Available prompts:\n")
    for key in memory:
        print("-", key)

    print("\nType a prompt (or 'exit'):\n")

    while True:
        user_input = input("Prompt: ").strip()

        if user_input.lower() == "exit":
            break

        if user_input in memory:
            print("\n📌 Stored TODOs:\n")
            for t in memory[user_input]:
                print("-", t["task"])
        else:
            print("❌ Prompt not found.\n")
