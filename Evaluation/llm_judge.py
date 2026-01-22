import time
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from groq import RateLimitError


judge_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

prompt_template = PromptTemplate.from_template(
    """
You are an evaluator.

Task:
{task}

Generated steps:
{steps}

Score the quality of task decomposition from 1 to 5.
Return ONLY the number.
"""
)


def evaluate(task: str, steps: list[str], retries: int = 3):
    prompt = prompt_template.format(
        task=task,
        steps="\n".join(steps)
    )

    for attempt in range(retries):
        try:
            response = judge_llm.invoke(prompt)
            return int(response.content.strip())
        except RateLimitError:
            wait = 5 * (attempt + 1)
            print(f"⚠️ Rate limit hit. Retrying in {wait}s...")
            time.sleep(wait)

    return 0  # fallback if all retries fail
