from experiment import run_single_experiment
from langsmith_gemini_eval import evaluate_report

DATASET = [
    "Write a research report on green hydrogen",
    "Create a financial outlook on renewable energy",
]

if __name__ == "__main__":

    for task in DATASET:
        print(f"\nRunning: {task}\n")

        report = run_single_experiment(task)
        evaluation = evaluate_report(report)

        print("Evaluation:")
        print(evaluation)
