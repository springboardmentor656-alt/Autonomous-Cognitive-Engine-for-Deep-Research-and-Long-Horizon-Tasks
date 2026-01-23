from langchain_groq import ChatGroq
import os

def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )
