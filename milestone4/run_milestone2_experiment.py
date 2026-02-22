# -------------------------------------------------
# LOAD ENV VARIABLES
# -------------------------------------------------
from dotenv import load_dotenv
load_dotenv()

# -------------------------------------------------
# IMPORTS
# -------------------------------------------------
from langsmith import evaluate
from agent.react_agent import app
from langchain_community.chat_models import ChatOllama

judge_llm = ChatOllama(
    model="llama3",
    temperature=0
)

# -------------------------------------------------
# AGENT RUNNER (LANGSMITH NEEDS THIS)
# -------------------------------------------------
def agent_runner(example):

    state = {
        "messages": [
            {"role": "user", "content": example["input"]}
        ],
        "todos": [],
        "files": {},
        "needs_read": False
    }

    result = app.invoke(state)

    final = result.get("final_output")

    if not final:
        final = "No final_output found. Full state:\n" + str(result)

    return {"output": final}


# -------------------------------------------------
# CUSTOM GEMINI JUDGE FUNCTION
# -------------------------------------------------
def quality_evaluator(run, example):

    user_input = example.inputs.get("input", "")
    agent_output = run.outputs.get("final_output", "")

    prompt = f"""
You are grading an AI research agent.

User request:
{user_input}

Agent output:
{agent_output}

Score from 1 to 10 based on:
- completeness
- clarity
- structure
- usefulness

Return ONLY a number.
"""

    response = judge_llm.invoke(prompt)

    try:
        score = int(response.content.strip())
    except:
        score = 0

    return {"score": score}



    response = judge_llm.invoke(prompt)

    try:
        score = int(response.content.strip())
    except:
        score = 3

    return {"score": score}


# -------------------------------------------------
# RUN LANGSMITH EXPERIMENT
# -------------------------------------------------
evaluate(
    agent_runner,
    data="milestone-2-vfs-ui-comparison",
    experiment_prefix="milestone-4-evaluation",
    evaluators=[quality_evaluator]
)

print("✅ Experiment finished. Check LangSmith → Experiments")
