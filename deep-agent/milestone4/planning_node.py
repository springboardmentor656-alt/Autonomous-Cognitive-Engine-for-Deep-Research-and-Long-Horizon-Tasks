from langchain_ollama import ChatOllama

llm = ChatOllama(model="tinyllama", temperature=0)

def planning_node(state):

    user_input = state["messages"][-1]["content"]

    prompt = f"""
    Break the following request into 4-6 clear research tasks.
    Return as a numbered list.

    REQUEST:
    {user_input}
    """

    response = llm.invoke([{"role": "user", "content": prompt}])

    todos = []
    for line in response.content.split("\n"):
        if line.strip():
            todos.append(line.strip())

    state["todos"] = todos
    state["completed"] = False

    return state
