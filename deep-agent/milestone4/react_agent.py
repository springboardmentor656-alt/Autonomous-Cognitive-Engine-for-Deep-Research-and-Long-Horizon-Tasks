from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0
)


@tool
def write_todos(task: str):
    """
    Break a complex task into 4-6 structured research subtasks.
    Returns a list of dictionaries with fields:
    - task: str
    - status: 'pending'
    """

    prompt = f"""
    Break this task into 4-6 research subtasks.
    Return as a Python list of dictionaries like:
    [
        {{"task": "...", "status": "pending"}}
    ]

    TASK:
    {task}
    """

    response = llm.invoke(prompt)

    try:
        todos = eval(response.content)
    except:
        todos = [{"task": task, "status": "pending"}]

    return todos
