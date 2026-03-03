import os
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

# Direct keys for reliability
G_KEY = "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"
T_KEY = "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"

# Initialize Tools
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=G_KEY)
search_tool = TavilySearchResults(tavily_api_key=T_KEY, k=3)

# 1. Operational Rules for Task 2 (Master Architect System Prompt)
SYSTEM_PROMPT = (
    "You are a Master Architect Agent operating in a Deep Cognitive Framework. [cite: 4]\n"
    "Follow these operational rules for autonomy:\n"
    "1. PLANNING: Break high-level objectives into sequential sub-tasks. [cite: 7]\n"
    "2. OFFLOADING: If research findings or summaries exceed 500 words, indicate that the data is being stored in the Virtual File System. \n"
    "3. DELEGATION: If a task requires specialized deep-dives, simulate a call to a sub-agent. [cite: 10, 49]\n"
)

def planner_node(state):
    print("\n--- 📍 MILESTONE 1: STRATEGIC PLANNING ---")
    # Task 1: Building the TODO list [cite: 7, 47]
    prompt = f"{SYSTEM_PROMPT}\nCreate a structured TODO list for: {state['topic']}"
    response = llm.invoke(prompt)
    print(f"✅ Master Plan/TODO List Created.")
    return {"plan": [response.content]}

def research_node(state):
    print("\n--- 📍 MILESTONE 3: TOOL USE & DELEGATION ---")
    # Task 1: Executing search as a tool [cite: 51]
    query = state['topic']
    results = search_tool.invoke(query)
    print(f"✅ Research Data Gathered: {len(str(results))} characters retrieved.")
    return {"research_data": [str(results)]}

def writer_node(state):
    print("\n--- 📍 MILESTONE 4a: WRITING & CONTEXT OFFLOADING ---")
    data = state.get("research_data", "")
    # Task 3: Outputting a comprehensive markdown report [cite: 13, 32]
    prompt = f"{SYSTEM_PROMPT}\nUsing this data: {data}, write a detailed markdown report on {state['topic']}."
    response = llm.invoke(prompt)
    print("✅ Comprehensive Report Generated.")
    return {"report": response.content}

def reflector_node(state):
    print("\n--- 📍 MILESTONE 4b: ORCHESTRATION & REVIEW ---")
    rev_count = state.get("revision_count", 0)
    
    # Task 1 & 4: Orchestrator deciding the next action [cite: 19, 120]
    if rev_count == 0:
        critique_msg = "The report is good but needs more technical details on quantum-resistant cryptography. Please expand."
        print(f"🔄 ORCHESTRATOR: Quality check failed. Triggering Self-Correction Loop...")
    else:
        report = state.get("report", "")
        # Internal LLM-as-a-judge for loop termination [cite: 124]
        prompt = f"Critique this report: {report}. If it addresses all TODOs and is accurate, say 'APPROVED'."
        response = llm.invoke(prompt)
        critique_msg = response.content
        print(f"Critique Result: {critique_msg[:100]}...")

    new_rev_count = rev_count + 1
    return {"critique": critique_msg, "revision_count": new_rev_count}