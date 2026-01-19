import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuration management for the Financial Planning Agent"""
    

    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
    LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "financial-planning-agent")
    PROMPT_STYLE: str = os.getenv("PROMPT_STYLE", "default") 
    

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))

    MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "15"))
    MAX_TODOS = int(os.getenv("MAX_TODOS", "10"))
    
    @classmethod
    def validate(cls):
        """Validate that required environment variables are set"""
        missing = []
        
        if not cls.GROQ_API_KEY:
            missing.append("GROQ_API_KEY")
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        print("Configuration validated successfully!")
        print(f"Project: {cls.LANGCHAIN_PROJECT}")
        print(f"Model: {cls.LLM_MODEL}")
        print(f"Tracing: {'Enabled' if cls.LANGCHAIN_TRACING_V2 == 'true' else 'Disabled'}")

settings = Settings()