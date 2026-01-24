# agent/prompts.py

"""
All prompts used by the Agentic AI system
Milestone 1 – Task Planning & Reasoning
"""

# 🔹 Prompt for breaking a task into TODO steps
TASK_PLANNER_PROMPT = """
You are an expert project manager and planning agent.

Your goal is to take a high-level user request and break it down into a comprehensive, actionable, and logical step-by-step plan.

Rules for your plan:
1. **Focus on Sub-tasks**: Break the main goal into specific, bite-sized components.
2. **Logical Flow**: Ensure steps follow a natural order (e.g., Setup -> Development -> Testing).
3. **Actionability**: Each step must start with an action verb (e.g., "Research", "Install", "Configure").
4. **No Execution**: Do NOT explain how to do the steps or provide code. ONLY provide the steps.
5. **Format**: Return the steps as a clean, numbered list.

Task:
{task}

Provide the numbered plan below:
"""

# Alias for easier usage
PLANNER_PROMPT = TASK_PLANNER_PROMPT

# 🔹 Prompt for explaining a topic simply (used for demo / testing)
SIMPLE_EXPLAIN_PROMPT = """
Explain the following topic in SIMPLE language
using exactly 4 clear points.

Rules:
- Use easy words
- No long paragraphs
- Exactly 4 numbered points

Topic:
{task}
"""

# 🔹 Prompt used in ReAct reasoning loop
REACT_REASON_PROMPT = """
You are a reasoning agent.

Think step by step about the current TODO item.
Decide what action should be taken next.

Current task:
{task}

Current TODO:
{todo}

Think clearly before acting.
"""

# 🔹 Prompt for executing a TODO item
EXECUTION_PROMPT = """
You are executing a task. Think step by step.

Current task:
{task}

Current TODO:
{todo}

Decide and describe the next action clearly.
"""

# -----------------------------
# Helper functions to format prompts
# -----------------------------

def get_task_plan(task):
    """Return the formatted planning prompt for a task."""
    return PLANNER_PROMPT.format(task=task)

def get_simple_explanation(topic):
    """Return the formatted simple explanation prompt for a topic."""
    return SIMPLE_EXPLAIN_PROMPT.format(task=topic)

def get_react_prompt(task, todo):
    """Return the formatted ReAct reasoning prompt."""
    return REACT_REASON_PROMPT.format(task=task, todo=todo)

def get_execution_prompt(task, todo):
    """Return the formatted execution prompt for a TODO item."""
    return EXECUTION_PROMPT.format(task=task, todo=todo)

# -----------------------------
# Demo (for testing)
# -----------------------------
if __name__ == "__main__":
    example_task = "Build a weather app using Python and Flask"

    print("=== Task Planner Prompt ===")
    print(get_task_plan(example_task))

    print("\n=== Simple Explanation Prompt ===")
    print(get_simple_explanation("How does a weather API work?"))

    print("\n=== ReAct Reasoning Prompt ===")
    print(get_react_prompt(example_task, "Set up Flask project structure"))

    print("\n=== Execution Prompt ===")
    print(get_execution_prompt(example_task, "Set up Flask project structure"))

