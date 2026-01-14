"""
LLM-as-a-Judge Evaluator for Task Planning Quality

This evaluator uses another LLM to judge whether the agent created
a good task plan.
"""

import sys
sys.path.append('..')

from langsmith import Client
from langsmith.evaluation import evaluate
from langchain_groq import ChatGroq
from config.settings import settings

JUDGE_PROMPT = """You are evaluating the quality of a financial planning agent's task breakdown.

The agent was given this request:
{input}

The agent created this task plan:
{output}

Evaluate whether this task plan is:
1. COMPREHENSIVE: Does it cover all aspects of the user's request?
2. SPECIFIC: Are the tasks actionable and clear (not vague)?
3. LOGICAL: Are tasks in a sensible order?
4. APPROPRIATE: Are these reasonable steps for a financial planner?

Respond with a score from 0.0 to 1.0:
- 1.0 = Excellent (meets all criteria perfectly)
- 0.7-0.9 = Good (meets most criteria)
- 0.4-0.6 = Acceptable (meets some criteria)
- 0.0-0.3 = Poor (fails most criteria)

Then explain your reasoning in 1-2 sentences."""

def create_evaluator():
    """
    Create an LLM-based evaluator that judges task quality.
    """
    
    judge_llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=0.0, 
        groq_api_key=settings.GROQ_API_KEY
    )
    
    def evaluate_task_quality(run, example):
        """Custom evaluator function"""
        user_request = example.inputs.get("user_request", "")
        todos = run.outputs.get("todos", [])
        
        formatted_tasks = format_todos(todos)

        eval_prompt = JUDGE_PROMPT.format(
            input=user_request,
            output=formatted_tasks
        )
        
        try:
            response = judge_llm.invoke(eval_prompt)
            result_text = response.content
 
            import re
            score_match = re.search(r'(\d+\.?\d*)', result_text)
            if score_match:
                score = float(score_match.group(1))
                # Normalize if needed
                if score > 1.0:
                    score = score / 10.0
                score = max(0.0, min(1.0, score))
            else:
                score = 0.5 
            
            return {
                "key": "task_quality",
                "score": score,
                "comment": result_text
            }
        except Exception as e:
            print(f"Evaluation error: {e}")
            return {
                "key": "task_quality", 
                "score": 0.0,
                "comment": f"Error: {str(e)}"
            }
    
    evaluate_task_quality.key = "task_quality"
    
    return evaluate_task_quality

def format_todos(todos):
    """Format TODO list for judge to read"""
    if not todos:
        return "No tasks generated"
    
    formatted = []
    for i, todo in enumerate(todos, 1):
        desc = todo.get('description', 'No description')
        formatted.append(f"{i}. {desc}")
    
    return "\n".join(formatted)

def run_langsmith_evaluation(dataset_name="financial-planning-milestone1"):
    """
    Run evaluation using LangSmith's evaluation framework.
    
    This is more advanced than the basic evaluation script.
    It uses LLM-as-a-judge to score task quality.
    """
    
    print("=" * 70)
    print("LLM-AS-A-JUDGE EVALUATION")
    print("=" * 70)
    
    client = Client()
    
    try:
        dataset = client.read_dataset(dataset_name=dataset_name)
        print(f"Found dataset: {dataset_name}")
        print(f"Examples in dataset: {len(list(client.list_examples(dataset_id=dataset.id)))}")
    except Exception as e:
        print(f"Dataset not found: {dataset_name}")
        print(f"\nRun this first: python tests/upload_dataset_to_langsmith.py")
        return
    
    print("\nLoading agent...")
    from agents.main_agent import financial_agent
    from state.agent_state import create_initial_state
    
    def run_agent(inputs):
        """Wrapper function for evaluation"""
        try:
            state = create_initial_state(inputs["user_request"], max_iterations=5)
            result = financial_agent.invoke(state)
            return {"todos": result.get("todos", [])}
        except Exception as e:
            print(f"Agent error: {e}")
            return {"todos": []}
    
    print("Creating LLM judge...")
    evaluator = create_evaluator()
    
    print("\nRunning evaluation...")
    print("This will:")
    print("  1. Run your agent on all test cases")
    print("  2. Ask an LLM judge to score each result")
    print("  3. Calculate overall success rate")
    print("\nThis may take a few minutes...\n")
    
    try:
        results = evaluate(
            run_agent,
            data=dataset_name,
            evaluators=[evaluator],
            experiment_prefix="milestone1-judge",
            description="LLM-as-a-judge evaluation of task planning",
            max_concurrency=1
        )
        
        print("\n" + "=" * 70)
        print("EVALUATION COMPLETE")
        print("=" * 70)
        
        try:
            aggregate_results = results.to_pandas()
            if 'task_quality' in aggregate_results.columns:
                avg_score = aggregate_results['task_quality'].mean()
                print(f"\nAverage Quality Score: {avg_score:.2f}/1.0")
                print(f"Success Rate: {(avg_score * 100):.1f}%")
        except:
            pass
        
        print(f"\nView detailed results in LangSmith:")
        print(f"   https://smith.langchain.com/")
        print(f"\nNavigate to: Datasets → {dataset_name} → Experiments")
        print("=" * 70)
        
        return results
        
    except Exception as e:
        print(f"\nEvaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    try:
        settings.validate()
        run_langsmith_evaluation()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()