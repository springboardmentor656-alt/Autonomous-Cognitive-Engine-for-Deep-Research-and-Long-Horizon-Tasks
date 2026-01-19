from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from tools.file_system_tools import FILE_SYSTEM_TOOLS
from config.settings import settings

def execute_todo(state):
    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        groq_api_key=settings.GROQ_API_KEY
    ).bind_tools(FILE_SYSTEM_TOOLS)


    current_todo = next(
        (t for t in state["todos"] if t["status"] == "pending"),
        None
    )


    if not current_todo:
        return {}

    prompt = f"""
You are executing this task:

TASK: {current_todo['description']}

Available files:
{list(state["files"].keys())}

STRICT RULES:
1. If you need a file, use:
   read_file(filename="example.txt")

2. To update a file:
   edit_file(filename="example.txt", content="new content")

3. To create a file:
   write_file(filename="example.txt", content="text")

4. NEVER use XML, JSON, or <function=...> formats.
5. Only use the exact tool call syntax shown above.
"""

    response = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content="Execute the task.")
    ])

    current_todo["status"] = "completed"
    current_todo["result"] = "Task executed using file system tools."

    return {
        "messages": [response],
        "todos": state["todos"]
    }
