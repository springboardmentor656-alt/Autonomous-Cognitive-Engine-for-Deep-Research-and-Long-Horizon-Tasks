from agent.supervisor import supervisor_agent
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "autonomous-cognitive-engine"

user_task = input("Enter a complex task: ")

agent_state = supervisor_agent(user_task)

print("\nGenerated TODO List:")
for i, todo in enumerate(agent_state["todos"], start=1):
    print(f"{i}. {todo}")
