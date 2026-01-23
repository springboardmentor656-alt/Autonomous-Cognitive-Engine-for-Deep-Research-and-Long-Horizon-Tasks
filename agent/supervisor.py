from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agent.sub_agents.summarizer import summarization_agent

load_dotenv()

# ---------------- LLM ----------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

# ---------------- PLANNER CHAIN ----------------
planner_prompt = ChatPromptTemplate.from_template(
    """
You are a planning agent.
Break the given task into a clear, ordered TODO list.
Return only the steps, one per line.

Task:
{task}
"""
)

planner_chain = planner_prompt | llm

# ---------------- EXECUTOR CHAIN ----------------
executor_prompt = ChatPromptTemplate.from_template(
    """
Execute the following task step clearly and concisely.

Step:
{step}
"""
)

executor_chain = executor_prompt | llm


def supervisor_agent(user_task: str):
    # -------- STATE --------
    state = {
        "task": user_task,
        "todos": [],
        "files": {}
    }

    # -------- PLANNING --------
    plan_result = planner_chain.invoke({"task": user_task})

    todos = [
        line.strip("•-0123456789. ")
        for line in plan_result.content.split("\n")
        if line.strip()
    ]

    state["todos"] = todos

    # -------- EXECUTION + DELEGATION --------
    for idx, todo in enumerate(todos, start=1):

        # 🔹 DELEGATION LOGIC (Milestone 3)
        if "summarize" in todo.lower():
            result = summarization_agent(todo)
        else:
            result = executor_chain.invoke({"step": todo}).content

        filename = f"step_{idx}.txt"
        state["files"][filename] = result

    return state
