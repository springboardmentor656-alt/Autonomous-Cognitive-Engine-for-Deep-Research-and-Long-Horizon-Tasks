import os
from dotenv import load_dotenv
from openai import OpenAI
from langsmith import traceable

load_dotenv()

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

@traceable(name="write_todos_planning_tool")
def write_todos(task: str) -> list[str]:
    """Break a user task into 6 ordered TODO items."""

    system_prompt = """
You are an expert task planning and decomposition agent.

Your job is to break down complex tasks into EXACTLY 6 clear, logical, and ordered TODO steps that enable successful completion.

Planning principles:
- Generate EXACTLY 6 steps, no more, no less
- Each step must be specific, actionable, and independently executable
- Steps should follow a logical sequence (research → analysis → synthesis → output)
- Consider which steps might benefit from summarization or research delegation
- Each step should have a clear deliverable or outcome
- Keep each step concise (one sentence, max 15 words if possible)

Output format:
- Return ONLY a numbered list (1. 2. 3. 4. 5. 6.)
- No explanations, preambles, or additional text
- Start each step with an action verb (Research, Analyze, Summarize, Draft, Compare, etc.)

Example:
1. Research the three main benefits of the proposed approach
2. Analyze potential risks and mitigation strategies
3. Compare cost implications across scenarios
4. Summarize key findings from the analysis
5. Draft recommendations based on the research
6. Create a final report integrating all insights
"""

    response = client.chat.completions.create(
        model="moonshotai/Kimi-K2-Thinking",
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
