from dotenv import load_dotenv
load_dotenv()

from agent.supervisor import run_tasks

test_cases = [
    "Analyze the impact of AI in healthcare and list 3 major companies involved.",
    "Research renewable energy trends and summarize the top 3 countries leading adoption.",
    "Evaluate current breakthroughs in quantum computing and list 3 companies advancing it."
]

print("Running Milestone 4 Evaluation Suite...\n")

run_tasks(test_cases)

print("\nEvaluation Suite Completed.")
