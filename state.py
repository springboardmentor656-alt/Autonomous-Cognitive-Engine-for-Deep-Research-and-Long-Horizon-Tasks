from typing import TypedDict, List

class AgentState(TypedDict):
    topic: str
    plan: List[str]
    research_data: List[str]
    report: str
    critique: str
    revision_count: int