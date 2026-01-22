from Evaluation.llm_judge import evaluate as llm_score

class PlanningAccuracyEvaluator:
    def __call__(self, run, example):
        task = example.inputs.get("task", "")

        # ✅ FIX: extract output correctly
        if isinstance(run.outputs, dict):
            todos_text = run.outputs.get("output", "")
        else:
            todos_text = run.outputs

        todos = [
            line.strip()
            for line in todos_text.split("\n")
            if line.strip()
        ]

        score = llm_score(task, todos)

        return {
            "key": "planning_accuracy",
            "score": score,
            "commentary": f"LLM judge score: {score}/5"
        }
