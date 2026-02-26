import os
import json
from typing import List, Dict, Any

from dotenv import load_dotenv
from groq import Groq
from langsmith import traceable

from agent_state import AgentState, Todo
from summarization_agent import summarization_graph

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# =========================================================
# SUB-AGENT REGISTRY (Extensible Architecture)
# =========================================================
SUBAGENT_REGISTRY = {
    "Summarization_Agent": summarization_graph,
    # Future:
    # "Research_Agent": research_graph,
    # "Financial_Agent": financial_graph,
}


def call_subagent(name: str, sub_state: AgentState) -> AgentState:
    graph = SUBAGENT_REGISTRY.get(name)
    if not graph:
        raise ValueError(f"Unknown sub-agent: {name}")
    return graph.invoke(sub_state)


# =========================================================
# MILESTONE 4 — INTELLIGENT PLANNING TOOL
# =========================================================
@traceable(name="write_todos_tool")
def writetodos_tool(user_request: str) -> List[Todo]:

    prompt = f"""
You are a strategic planning module for an autonomous research agent.

Goal:
\"\"\"{user_request}\"\"\"

Break this goal into 3–6 actionable tasks.

Rules:
- If a task requires deep analysis or summarization, include the word "Summarize".
- If a task requires collecting data or background information, include the word "Research".
- If a task requires producing the final output document, include the word "Write".

Return ONLY valid JSON in this format:

{{
  "todos": [
    {{"id": 1, "description": "Summarize core industry trends", "status": "pending"}}
  ]
}}
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500,
    )

    raw_output = completion.choices[0].message.content.strip()

    try:
        data = json.loads(raw_output)
    except Exception:
        start = raw_output.find("{")
        end = raw_output.rfind("}")
        if start != -1 and end != -1:
            data = json.loads(raw_output[start:end + 1])
        else:
            return [{
                "id": 1,
                "description": "Summarize the provided article",
                "status": "pending"
            }]

    return data.get("todos", [])


# =========================================================
# MILESTONE 3 — DELEGATION TOOL
# =========================================================
@traceable(name="delegate_task")
def delegate_task(
    state: AgentState,
    subagent_name: str,
    task_payload: Dict[str, Any],
) -> Dict[str, Any]:

    sub_state: AgentState = {
        "messages": [task_payload.get("text", "")],
        "todos": [],
        "files": {},
        "done": False,
    }

    final_sub_state = call_subagent(subagent_name, sub_state)

    return {
        "files": final_sub_state.get("files", {}),
        "messages": final_sub_state.get("messages", []),
        "done": final_sub_state.get("done", False),
    }


# =========================================================
# MILESTONE 4 — INTELLIGENT REPORT SYNTHESIS
# =========================================================
@traceable(name="generate_final_report")
def generate_final_report(files: Dict[str, str]) -> str:

    compiled_context = ""

    for fname, content in files.items():
        compiled_context += f"\n--- {fname} ---\n{content}\n"

    prompt = f"""
You are a professional industry analyst.

Using the research material below, generate a structured,
well-formatted industry report in markdown format.

Include:
- Executive Summary
- Industry Trends
- Competitive Landscape
- Strategic Risks
- Conclusion

Research Material:
\"\"\"
{compiled_context}
\"\"\"
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=900,
    )

    return completion.choices[0].message.content.strip()
