from agents.specialized.researcher import researcher_agent
from agents.specialized.summarizer import summarizer_agent

def task(type, content):
    if type == "research":
        return researcher_agent(content)
    else:
        return summarizer_agent(content)