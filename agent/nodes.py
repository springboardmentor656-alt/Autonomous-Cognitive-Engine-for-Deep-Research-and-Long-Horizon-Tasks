from langchain_core.prompts import ChatPromptTemplate
from agent.state import AgentState
from agent.llm import get_llm
from agent.tools.delegate import delegate_task


# ---------------- PLANNER ----------------
planner_prompt = ChatPromptTemplate.from_template(
    """
Break the task into a clear ordered TODO list.
Return one step per line.

Task:
{task}
"""
)

def plan_node(state: AgentState) -> AgentState:
    llm = get_llm()
    planner_chain = planner_prompt | llm

    result = planner_chain.invoke({"task": state["task"]})

    todos = []
    for line in result.content.split("\n"):
        line = line.strip()
        if len(line) > 5:
            todos.append(line)

    state["todos"] = todos
    return state


# ---------------- EXECUTOR ----------------
executor_prompt = ChatPromptTemplate.from_template(
    """
Execute this step clearly.

Step:
{step}
"""
)

def execute_node(state: AgentState) -> AgentState:
    llm = get_llm()
    executor_chain = executor_prompt | llm

    files = {}

    for i, step in enumerate(state.get("todos", []), start=1):
        if "summarize" in step.lower():
            result = delegate_task("summarization", step)
        else:
            result = executor_chain.invoke({"step": step}).content

        files[f"step_{i}.txt"] = result

    state["files"] = files
    return state


# ---------------- SYNTHESIZER ----------------
def synthesize_node(state: AgentState) -> AgentState:
    files = state.get("files", {})

    combined_output = ""
    for name, content in files.items():
        combined_output += f"\n\n{name}:\n{content}"

    state["final_output"] = combined_output.strip()
    return state
