# run_experiment.py

import os
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "agentic-ai-infosys"

# -----------------------------
# Imports AFTER env setup
# -----------------------------
from langsmith import Client
from langsmith.evaluation import evaluate
from graph.graph import build_graph
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from agent.evaluators import EVALUATION_PROMPT_TEMPLATE

# -----------------------------
# Initialize LangSmith client
# -----------------------------
client = Client()

# -----------------------------
# Build your agent graph
# -----------------------------
graph = build_graph()

# -----------------------------
# Function to safely extract input from dataset examples
# -----------------------------
def extract_user_input(example):
    """
    Robustly extract the task string from various LangChain/LangSmith dataset formats.
    """
    content = ""
    
    # 1. Handle "messages" field (common in LangChain evaluators)
    if "messages" in example:
        msg_data = example["messages"]
        
        # Unroll nesting (sometimes it's [[{...}]])
        while isinstance(msg_data, list) and len(msg_data) > 0:
            msg_data = msg_data[0]
            
        if isinstance(msg_data, dict):
            # Try content in kwargs or top-level content
            content = msg_data.get("kwargs", {}).get("content", "") or msg_data.get("content", "")

    # 2. Handle "task" field (direct entry)
    if not content and "task" in example:
        content = example["task"]

    # 3. Handle cases where the whole example is a string
    if not content and isinstance(example, str):
        content = example

    # 4. Post-processing: Extract "task" from JSON-like strings
    if isinstance(content, str):
        content_stripped = content.strip()
        if content_stripped.startswith("{") and content_stripped.endswith("}"):
            try:
                import json
                data = json.loads(content_stripped)
                if isinstance(data, dict):
                    return data.get("task", data.get("content", content))
            except:
                pass
        
        # If it contains "Topic: ...", extract the topic
        if "Topic:" in content:
            parts = content.split("Topic:")
            if len(parts) > 1:
                return parts[1].strip()

    return content or "No task provided"

# -----------------------------
# Agent runner for LangSmith evaluation
# -----------------------------
def agent_runner(example):
    user_input = extract_user_input(example)
    print(f"\n[RUNNER] Processing task: {user_input}")

    # Send input through your agent graph
    state = {"messages": [{"role": "user", "content": user_input}]}
    result = graph.invoke(state)
    print(f"[RUNNER] Result: {result.get('todos', [])[:2]}...")
    return result

# -----------------------------
# LLM test (offline check)
# -----------------------------
def test_model():
    from agent.config import get_model_name, get_api_key, PRIMARY_PROVIDER
    model = get_model_name()
    api_key = get_api_key()
    
    print(f"🚀 Testing {PRIMARY_PROVIDER} LLM ({model})...")
    
    if PRIMARY_PROVIDER == "groq":
        from langchain_groq import ChatGroq
        chat = ChatGroq(model=model, api_key=api_key)
    elif PRIMARY_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI
        chat = ChatOpenAI(model=model, api_key=api_key)
    elif PRIMARY_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic
        chat = ChatAnthropic(model=model, api_key=api_key)
    else:
        from langchain_groq import ChatGroq
        chat = ChatGroq(model=model, api_key=api_key)
        
    response = chat.invoke([HumanMessage(content="Explain ML in simple language using 4 points")])
    print(f"{PRIMARY_PROVIDER} test output: {response.content[:100]}...")

# -----------------------------
# Run a small Groq test
# -----------------------------
if __name__ == "__main__":
    test_model()

    # -----------------------------
    # Custom Evaluator for LangSmith
    # -----------------------------
    def task_plan_evaluator(run, example):
        """
        Comprehensive evaluator that returns multiple keys for dashboard alignment.
        """
        from agent.evaluators import PlanEvaluator, EvaluationResult
        evaluator = PlanEvaluator()
        
        user_request = extract_user_input(example)
        
        # Robustly get output from either our agent (todos) or a raw model run (output/text/string)
        if isinstance(run.outputs, dict):
            generated_plan = run.outputs.get("todos") or run.outputs.get("output") or run.outputs.get("text") or run.outputs.get("answer")
        else:
            generated_plan = run.outputs

        result = evaluator.evaluate(user_request, generated_plan)
        
        if result:
            s = result.overall if isinstance(result, EvaluationResult) else result.get("overall", 0.0)
            return {
                "results": [
                    {"key": "task_plan_quality", "score": float(s)},
                    {"key": "score", "score": float(s)},
                    {"key": "correctness", "score": float(s)},
                ],
                "comment": str(result)
            }
        return {"score": 0.0, "comment": "Evaluation failed"}

    # -----------------------------
    # Run LangSmith evaluation
    # -----------------------------
    print(f"🚀 Running LangSmith Experiment: stupendous-cloth-23-SOLVED...")
    evaluate(
        agent_runner,
        data="ds-granular-oleo-34",
        client=client,
        evaluators=[task_plan_evaluator],
        experiment_prefix="stupendous-cloth-23-SOLVED"
    )

    print("\n✅ Experiment completed! Check LangSmith dashboard")
