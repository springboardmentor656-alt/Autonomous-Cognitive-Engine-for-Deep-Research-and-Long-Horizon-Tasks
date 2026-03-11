import os
from dotenv import load_dotenv

from agent.supervisor import supervisor_agent


load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "autonomous-cognitive-engine-use-case"


DEFAULT_TASK = (
    "Generate an autonomous research brief on AI agents in education, "
    "including latest trends, key opportunities, risks, and practical recommendations."
)


def run_autonomous_research(task: str = DEFAULT_TASK) -> dict:
    """Run the primary autonomous research use case and return final state."""
    return supervisor_agent(task)


if __name__ == "__main__":
    state = run_autonomous_research()
    print("Use case run complete")
    print(f"Status: {state.get('status', 'unknown')}")
    print(f"Files generated: {len(state.get('files', {}))}")
