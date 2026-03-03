import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable

# Hardcoded Key for guaranteed authentication
GROQ_KEY = "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"

@traceable(name="Summarizer_SubAgent")
def summarizer_agent(content: str):
    """
    Milestone 3: Specialized Sub-Agent for synthesis.
    Takes raw research notes and turns them into a structured report.
    """
    # Using the updated model name and hardcoded key
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile", 
        groq_api_key=GROQ_KEY,
        temperature=0.2
    )
    
    print(f"  [SUMMARIZER] 📝 Synthesizing research ({len(content)} characters)...")
    
    prompt = ChatPromptTemplate.from_template("""
    You are a Senior Technical Writer. 
    Your goal is to take the following raw research notes and create a 
    comprehensive, professional report.
    
    RAW NOTES:
    {content}
    
    REPORT REQUIREMENTS:
    1. Use clear headings (Executive Summary, Key Findings, Risks, Recommendations).
    2. Use bullet points for readability.
    3. Focus on the impact by the year 2030.
    4. Maintain a professional, objective tone.
    """)
    
    chain = prompt | llm
    response = chain.invoke({"content": content})
    
    return response.content