import os
from dotenv import load_dotenv
from openai import OpenAI
from langsmith import traceable

load_dotenv()

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)


@traceable(name="researcher_agent")
def research_agent(question: str) -> str:
    """Generate a structured research response for a question."""

    system_prompt = """
You are an expert research assistant specializing in comprehensive information synthesis.

Your responsibilities:
- Provide thorough, well-researched answers with depth and accuracy
- Structure information logically with clear sections
- Include 4-7 key insights or findings as bullet points
- Cite relevant concepts, methodologies, or frameworks when applicable
- Distinguish between established facts and uncertain information
- Provide actionable insights or recommendations when relevant

Output format:
1. Brief introduction (1-2 sentences)
2. Main findings (bullet points or numbered list)
3. Key insights or implications
4. Brief conclusion with recommendations if applicable

Be comprehensive but concise. Focus on quality and actionable information."""

    response = client.chat.completions.create(
        model="moonshotai/Kimi-K2-Thinking",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.3,
        max_tokens=400
    )

    raw_choice = response.choices[0] if response and getattr(response, "choices", None) else None
    content = raw_choice.message.content if raw_choice and getattr(raw_choice, "message", None) else None
    return content.strip() if content else "Model returned empty content."
