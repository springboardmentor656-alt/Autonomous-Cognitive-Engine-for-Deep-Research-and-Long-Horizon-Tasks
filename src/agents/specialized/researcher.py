import os
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate

GROQ_KEY = "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"
TAVILY_KEY = "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"

# Initialize the tool with the hardcoded key
search_tool = TavilySearch(tavily_api_key=TAVILY_KEY, max_results=3)

def researcher_agent(task_description: str):
    """Sub-agent for web research."""
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile", 
        groq_api_key=GROQ_KEY
    )
    
    print(f"  [RESEARCHER] 🔍 Searching for: {task_description}")
    search_results = search_tool.invoke({"query": task_description})
    
    prompt = ChatPromptTemplate.from_template("""
    You are a Research Analyst. Summarize the following web data regarding: {task}
    
    Web Results:
    {results}
    
    Provide a factual, detailed summary.
    """)
    
    chain = prompt | llm
    response = chain.invoke({"task": task_description, "results": search_results})
    return response.content