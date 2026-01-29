import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# LLM Provider Configuration
# -----------------------------
# Options: "groq", "openai", "anthropic"
PRIMARY_PROVIDER = os.getenv("PRIMARY_LLM_PROVIDER", "groq")

# Model Names
GROQ_MODEL = "llama-3.3-70b-versatile"
OPENAI_MODEL = "gpt-4o-mini"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"

def get_model_name():
    if PRIMARY_PROVIDER == "groq":
        return GROQ_MODEL
    elif PRIMARY_PROVIDER == "openai":
        return OPENAI_MODEL
    elif PRIMARY_PROVIDER == "anthropic":
        return ANTHROPIC_MODEL
    return GROQ_MODEL

def get_api_key():
    if PRIMARY_PROVIDER == "groq":
        return os.getenv("GROQ_API_KEY")
    elif PRIMARY_PROVIDER == "openai":
        return os.getenv("OPENAI_API_KEY")
    elif PRIMARY_PROVIDER == "anthropic":
        return os.getenv("ANTHROPIC_API_KEY")
    return None
