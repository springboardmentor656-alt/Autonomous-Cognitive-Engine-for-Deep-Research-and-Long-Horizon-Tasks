# src/agents/specialized/__init__.py
from .researcher import researcher_agent
from .summarizer import summarizer_agent

# This tells Python which functions are 'public' in this sub-package
__all__ = ["researcher_agent", "summarizer_agent"]