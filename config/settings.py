import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuration management for the Financial Planning Agent"""
    
    # LangSmith Configuration
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
    LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "financial-planning-agent")
    
    # LLM Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    
    # ADD THIS LINE - Smaller model for sub-agents (5x more tokens/day!)
    SUB_AGENT_MODEL = os.getenv("SUB_AGENT_MODEL", "llama-3.1-8b-instant")
    
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0"))
    
    # Prompt style
    PROMPT_STYLE = os.getenv("PROMPT_STYLE", "default")
    
    # Agent Configuration
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