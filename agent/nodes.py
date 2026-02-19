from langchain_core.prompts import ChatPromptTemplate
from agent.state import AgentState
from agent.llm import get_llm
from agent.tools.delegate import delegate_task


# ---------------- PLANNER ----------------
planner_prompt = ChatPromptTemplate.from_template(
    """
You are an autonomous research agent.

Break the given task into a structured RESEARCH OUTLINE.
Each line must be a SECTION of a research report, not an action plan.
Only include sections directly related to the given topic.
Do NOT introduce unrelated technologies or domains.


Use sections such as:
- Introduction
- Background / Context
- Key Concepts
- Advantages
- Challenges
- Applications / Use Cases
- Conclusion

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
Write a detailed RESEARCH SECTION for the heading below.

Guidelines:
- Use an academic, explanatory tone
- Explain concepts clearly
- Do NOT write implementation steps or project plans
- Do NOT include bullet-point action items
- Keep it suitable for a research report

Section Heading:
{step}
"""
)


def execute_node(state: AgentState) -> AgentState:
    llm = get_llm()
    executor_chain = executor_prompt | llm

    todos = state.get("todos", [])
    current_step = state.get("current_step", 0)
    files = state.get("files", {})

    print("EXECUTE → current_step:", current_step)

    if current_step < len(todos):
        step = todos[current_step]
        result = executor_chain.invoke({"step": step}).content

        files[f"step_{current_step+1}.txt"] = result
        state["files"] = files
        state["current_step"] = current_step + 1

        print("EXECUTE → incremented to:", state["current_step"])

    return state





# ---------------- SYNTHESIZER ----------------
def synthesize_node(state: AgentState) -> AgentState:
    files = state.get("files", {})

    final_report = "# Final Research Report\n\n"

    for name, content in files.items():
        final_report += f"\n\n## {name}\n{content}"

    state["files"]["final_report.md"] = final_report
    state["final_output"] = final_report

    return state


def orchestrator_node(state: AgentState) -> AgentState:
    todos = state.get("todos", [])
    current_step = state.get("current_step", 0)

    print("DEBUG → current_step:", current_step)
    print("DEBUG → total todos:", len(todos))

    if current_step >= len(todos):
        print("DEBUG → Moving to SYNTHESIZE")
        state["next_action"] = "synthesize"
    else:
        print("DEBUG → Moving to EXECUTE")
        state["next_action"] = "execute"

    return state



