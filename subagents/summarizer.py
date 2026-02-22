from langchain_groq import ChatGroq
from langsmith import traceable

# Initialize LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)


@traceable(name="Summarization Agent")
def run(task: str, research_content: str = "") -> str:

    if not research_content.strip():
        return "No research content was provided to summarize."

    # 🔥 TOKEN SAFETY LIMIT
    MAX_CHARS = 4000  # Prevent 413 token overflow

    if len(research_content) > MAX_CHARS:
        research_content = research_content[:MAX_CHARS]
        research_content += "\n\n[Note: Research content was truncated due to token limits.]"

    prompt = f"""
You are a professional AI report writer.

Your goal is to convert research findings into a structured, clear, and well-organized report.

Original Task:
{task}

Research Findings:
{research_content}

Generate a structured final report with:

1. Title
2. Introduction
3. Key Sections with Headings
4. Bullet Points where helpful
5. Clear Conclusion
6. Key Insights / Takeaways

Keep it professional, concise, and logically organized.
"""

    response = llm.invoke(prompt)
    return response.content
