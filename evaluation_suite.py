import argparse
import json
import os
from datetime import datetime
from statistics import mean

from dotenv import load_dotenv
from openai import OpenAI
from langsmith import traceable

from agent.supervisor import supervisor_agent


load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "autonomous-cognitive-engine-eval"


client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY"),
)


DEFAULT_TASKS = [
    "Generate a research report on AI agents in education with recommendations.",
    "Research and compare autonomous research frameworks for enterprise use.",
    "Summarize current trends in multi-agent orchestration and long-horizon planning.",
    "Analyze benefits and risks of AI copilots in software engineering teams.",
    "Compare LangGraph and similar orchestration approaches with practical guidance.",
    "Create a policy-oriented brief on AI safety practices for educational institutions.",
    "Research best practices for context management in LLM-based agents.",
    "Evaluate sub-agent delegation patterns and propose an implementation checklist.",
    "Write a concise strategy report on adopting AI assistants in higher education.",
    "Assess tooling for agent observability and recommend a monitoring approach.",
]


@traceable(name="llm_judge")
def judge_output(task: str, final_output: str) -> tuple[str, str]:
    """Return (rating, reason) where rating is excellent/good/fair/poor."""
    prompt = (
        "You are evaluating quality of an autonomous agent final output. "
        "Rate strictly as one of: excellent, good, fair, poor. "
        "Then give one short reason. "
        "Return JSON only: {\"rating\":\"...\",\"reason\":\"...\"}."
    )
    response = client.chat.completions.create(
        model="moonshotai/Kimi-K2-Thinking",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": f"Task:\n{task}\n\nFinal Output:\n{final_output}",
            },
        ],
        temperature=0.1,
        max_tokens=150,
    )

    content = response.choices[0].message.content.strip()
    try:
        data = json.loads(content)
        rating = str(data.get("rating", "fair")).lower()
        reason = str(data.get("reason", "No reason provided."))
    except Exception:
        lowered = content.lower()
        if "excellent" in lowered:
            rating = "excellent"
        elif "good" in lowered:
            rating = "good"
        elif "poor" in lowered:
            rating = "poor"
        else:
            rating = "fair"
        reason = "Fallback parse from model text."
    return rating, reason


def heuristic_rating(state: dict) -> tuple[str, str]:
    """Simple fallback quality proxy when LLM judging is disabled."""
    output = (state.get("final_output") or "").strip()
    completed = len(state.get("completed_todos", []))
    todos = len(state.get("todos", []))
    if todos > 0 and completed == todos and len(output) > 700:
        return "good", "Completed all TODOs with substantial final output."
    if todos > 0 and completed >= max(1, todos - 1) and len(output) > 350:
        return "fair", "Mostly complete with moderate output detail."
    return "poor", "Incomplete execution or very short final output."


def evaluate_tasks(tasks: list[str], use_llm_judge: bool) -> dict:
    results = []
    for idx, task in enumerate(tasks, start=1):
        state = supervisor_agent(task)
        status = state.get("status", "unknown")
        error = (state.get("error") or "").strip()
        completed = len(state.get("completed_todos", []))
        total = len(state.get("todos", []))
        completion_ok = status == "complete" and completed == total and not error

        if use_llm_judge:
            rating, reason = judge_output(task, state.get("final_output", ""))
        else:
            rating, reason = heuristic_rating(state)

        results.append(
            {
                "id": idx,
                "task": task,
                "status": status,
                "completed_todos": completed,
                "total_todos": total,
                "error": error,
                "completion_ok": completion_ok,
                "rating": rating,
                "judge_reason": reason,
            }
        )

    completion_rate = mean([1.0 if r["completion_ok"] else 0.0 for r in results]) * 100
    quality_rate = (
        mean([1.0 if r["rating"] in {"good", "excellent"} else 0.0 for r in results])
        * 100
    )

    return {
        "total_tasks": len(results),
        "completion_rate_percent": round(completion_rate, 2),
        "good_or_excellent_percent": round(quality_rate, 2),
        "success_criteria_completion_met": completion_rate >= 70.0,
        "success_criteria_quality_met": quality_rate >= 70.0,
        "results": results,
    }


def save_report(report: dict) -> str:
    out_dir = os.path.join("output", "evaluations")
    os.makedirs(out_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(out_dir, f"evaluation_{stamp}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run end-to-end evaluation suite.")
    parser.add_argument("--tasks", type=int, default=10, help="Number of tasks to run (max 10).")
    parser.add_argument(
        "--judge",
        action="store_true",
        help="Use LLM-as-a-judge for output quality.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    task_count = max(1, min(args.tasks, len(DEFAULT_TASKS)))
    tasks = DEFAULT_TASKS[:task_count]

    report = evaluate_tasks(tasks, use_llm_judge=args.judge)
    report_path = save_report(report)

    print("Evaluation complete")
    print(f"Tasks run: {report['total_tasks']}")
    print(f"Completion rate: {report['completion_rate_percent']}%")
    print(f"Good/Excellent: {report['good_or_excellent_percent']}%")
    print(f"Completion criteria met (>70%): {report['success_criteria_completion_met']}")
    print(f"Quality criteria met (>70%): {report['success_criteria_quality_met']}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
