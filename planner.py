from langchain_groq import ChatGroq
import os


# Create LLM instance
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0
)


def planning_node(state):

    task = state["task"]

    prompt = f"""
You are an autonomous research strategist.

Break the following complex goal into 4–6 logical research tasks.

Goal:
{task}

Return numbered steps only.
"""

    response = llm.invoke(prompt)

    todos = []
    for line in response.content.split("\n"):
        if line.strip() and line[0].isdigit():
            todos.append(line.split(".", 1)[1].strip())

    state["todos"] = todos
    state["current_index"] = 0

    return state
