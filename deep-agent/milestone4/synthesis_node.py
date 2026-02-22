from langchain_ollama import ChatOllama

# 🔥 Use a stronger model than tinyllama
llm = ChatOllama(
    model="llama3",   # change if needed: mistral / phi3
    temperature=0
)

def synthesis_node(state):
    """
    Final synthesis node.
    Combines all research files and generates a complete structured industry report.
    """

    # 1️⃣ Combine all research files
    combined_research = ""

    for filename, content in state["files"].items():
        if filename != "final_report.txt":
            combined_research += f"\n\n---\nSource: {filename}\n{content}\n"

    # 2️⃣ Strong synthesis prompt (forces long structured output)
    prompt = f"""
You are a senior industry analyst.

Using ONLY the research material provided below,
generate a COMPLETE professional industry report.

STRICT REQUIREMENTS:
- Minimum 1200 words
- Use clear structured headings
- Include:
    • Executive Summary
    • Introduction
    • Industry Background
    • Key Applications
    • Advantages
    • Disadvantages
    • Challenges
    • Practical Solutions
    • Future Outlook
    • Strong Conclusion
- Maintain a professional analytical tone
- Do NOT summarize
- Expand each section in detail

Research Material:
{combined_research}

Now generate the FULL final report.
"""

    # 3️⃣ Generate final report
    response = llm.invoke(prompt)

    final_report = response.content

    # 4️⃣ Save to virtual file system
    state["files"]["final_report.txt"] = final_report

    # 5️⃣ Also return output for LangSmith visibility
    return {
        "files": state["files"],
        "output": final_report
    }
