from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

def write_todos(task: str):
    prompt = f"""
You are a planning assistant.

Break the following task into clear, ordered TODO steps.
Return ONLY a numbered list.

Task: {task}
"""
    response = llm.invoke(prompt)

    todos = []
    for line in response.content.split("\n"):
        line = line.strip().lstrip("0123456789.- ").strip()
        if line:
            todos.append(line)

    return todos


if __name__ == "__main__":
    test_tasks = [
        "Build a smart traffic management system",
        "Create an AI-based resume screening tool",
        "Research cybersecurity threats in cloud computing",
        "Design a recommendation system for e-commerce",
        "Analyze the impact of AI in education"
    ]

    for task in test_tasks:
        print("\n========================================")
        print(f"Task: {task}")
        print("========================================\n")

        todos = write_todos(task)
        for i, todo in enumerate(todos, start=1):
            print(f"{i}. {todo}")
