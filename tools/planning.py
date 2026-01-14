import os
from dotenv import load_dotenv
from openai import OpenAI
from langsmith import traceable

# Load environment variables
load_dotenv()

# Initialize Nebius OpenAI-compatible client
client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

@traceable(name="write_todos_planning_tool")
def write_todos(task: str):
    """
    AI-powered planning tool.
    Decomposes a complex task into EXACTLY 6 ordered TODO steps.
    """

    system_prompt = """
You are an expert planning agent.

Your job is to break a complex user task into EXACTLY 6 clear, logical,
and ordered TODO steps.

Rules:
- Generate EXACTLY 6 steps, no more, no less
- Each step must be short and actionable (one sentence max)
- Steps must be ordered logically
- Do NOT include explanations or additional text
- Return ONLY a numbered list (1. 2. 3. 4. 5. 6.)
"""

    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-Coder-7B-fast",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task}
        ],
        temperature=0.2
    )

    raw_output = response.choices[0].message.content.strip()

    todos = []
    for line in raw_output.split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            parts = line.split(".", 1)
            if len(parts) > 1:
                todos.append(parts[1].strip())

    return todos[:6]
