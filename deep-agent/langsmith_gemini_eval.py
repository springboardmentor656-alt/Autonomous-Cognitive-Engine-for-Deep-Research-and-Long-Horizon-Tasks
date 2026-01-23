from dotenv import load_dotenv
load_dotenv()

import json
from langsmith import Client
from langsmith.evaluation import evaluate, RunEvaluator
from langchain_google_genai import ChatGoogleGenerativeAI
from agent.react_agent import app


class PlanningAccuracyEvaluator(RunEvaluator):
    def evaluate_run(self, run, example, **kwargs):
        user_request = example["input"]
        todos = run.outputs["output"]

        eval_prompt = f"""
You are evaluating a task-planning agent.

User request:
{user_request}

Generated TODO list:
{json.dumps(todos, indent=2)}

Score from 0 to 1 for:
- relevance
- completeness
- clarity
- actionability

Return ONLY valid JSON:
{{
  "relevance": number,
  "completeness": number,
  "clarity": number,
  "actionability": number,
  "overall": number
}}
"""

        response = judge_llm.invoke(eval_prompt)
        scores = json.loads(response.content)

        return {
            "key": "planning_accuracy",
            "score": scores["overall"],
            "commentary": json.dumps(scores)
        }