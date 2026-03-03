from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import json

def write_todos(topic: str, api_key: str):
    """Generates a JSON research plan using the new Llama 3.3 model."""
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile", 
        groq_api_key=api_key,
        temperature=0
    )
    
    prompt = ChatPromptTemplate.from_template("""
    You are a project manager. Create a 3-step research plan for: {topic}
    
    Format the output as a JSON list of objects:
    [
        {{"task": "Search for X", "status": "pending"}},
        {{"task": "Research Y", "status": "pending"}},
        {{"task": "Summarize findings into a report", "status": "pending"}}
    ]
    Return ONLY the JSON.
    """)
    
    chain = prompt | llm
    response = chain.invoke({"topic": topic})
    
    # Clean output in case LLM adds markdown backticks
    clean_json = response.content.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)