"""
LLM-as-a-Judge Evaluator for Milestone 4: Complete Financial Planning System

This evaluator uses Groq to judge the quality of end-to-end financial plans.

It evaluates:
- Completeness (all aspects addressed)
- Specificity (numbers, timelines, actionable steps)
- Integration (multi-domain synthesis)
- Professional quality
"""

import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from langsmith import Client
from langsmith.evaluation import evaluate
from langchain_groq import ChatGroq
from config.settings import settings

M4_JUDGE_PROMPT = """You are evaluating a complete end-to-end financial planning system.

USER REQUEST:
{input}

AGENT'S OUTPUT:
Number of files created: {file_count}
Number of specialist consultations: {delegation_count}
Files: {files}

FINAL PLAN CONTENT:
{final_plan}

EVALUATION CRITERIA:

1. COMPLETENESS (0-3 points)
   - Does it address ALL aspects of the user's request?
   - Are all financial domains covered (debt, budget, investment, etc.)?
   - Is there a comprehensive final plan?

2. SPECIFICITY (0-3 points)
   - Does it include actual numbers (dollar amounts, percentages)?
   - Are there specific timelines?
   - Are the steps actionable and clear?

3. MULTI-DOMAIN INTEGRATION (0-2 points)
   - Did it consult multiple specialists appropriately?
   - Is there evidence of cross-domain synthesis?
   - Are specialist insights integrated coherently?

4. PROFESSIONAL QUALITY (0-2 points)
   - Is the final plan well-organized?
   - Is the language clear and professional?
   - Would this be useful to a real client?

SCORING:
- Add up points across all criteria (max 10 points)
- Convert to 0.0-1.0 scale (divide by 10)
- 0.8-1.0 = Excellent
- 0.6-0.79 = Good
- 0.4-0.59 = Acceptable
- 0.0-0.39 = Poor

Respond EXACTLY in this format:
SCORE: [0.0 to 1.0]
RATING: [Excellent/Good/Acceptable/Poor]
REASON: [2-3 sentence explanation]

Example:
SCORE: 0.85
RATING: Excellent
REASON: The plan comprehensively addresses all five financial goals with specific dollar amounts and timelines. Multiple specialists were consulted (debt, budget, investment) and their insights were well-integrated into a coherent final plan. The output is professional and immediately actionable."""

def create_m4_evaluator():
    """
    Create an LLM-based evaluator for M4 outputs.
    Uses Groq's 8B model to save tokens.
    """
    
    judge_llm = ChatGroq(
        model=settings.SUB_AGENT_MODEL,  # Use smaller model to save tokens
        temperature=0.0,  # Deterministic judging
        groq_api_key=settings.GROQ_API_KEY
    )
    
    def evaluate_m4_quality(run, example):
        """Custom evaluator function for M4"""
        user_request = example.inputs.get("user_request", "")
        
        # Extract outputs
        outputs = run.outputs if run.outputs else {}
        files = outputs.get("files", {})
        todos = outputs.get("todos", [])
        
        
        # Find final plan
        final_plan = ""
        for filename, content in files.items():
            if 'final' in filename.lower() or 'comprehensive' in filename.lower():
                final_plan = content
                break
        
        if not final_plan:
            # Use the longest file as proxy for final plan
            final_plan = max(files.values(), key=len) if files else "No plan generated"
        
        # Format file list
        file_list = ", ".join(files.keys()) if files else "None"
        
        # Build evaluation prompt
        eval_prompt = f"""
        Evaluate this financial plan.

        USER REQUEST:
        {user_request}

        FINAL PLAN:
        {final_plan[:600]}

        Score 0–1.

        Format:
        SCORE:
        RATING:
        REASON:
        """

        
        try:
            response = judge_llm.invoke(eval_prompt)
            result_text = response.content
            
            # Parse response
            import re
            
            score_match = re.search(r'SCORE:\s*(\d+\.?\d*)', result_text)
            rating_match = re.search(r'RATING:\s*(\w+)', result_text)
            reason_match = re.search(r'REASON:\s*(.+?)(?:\n\n|$)', result_text, re.DOTALL)
            
            score = float(score_match.group(1)) if score_match else 0.5
            rating = rating_match.group(1) if rating_match else "Unknown"
            reason = reason_match.group(1).strip() if reason_match else result_text
            
            # Normalize score
            if score > 1.0:
                score = score / 10.0
            score = max(0.0, min(1.0, score))
            
            return {
                "key": "m4_quality",
                "score": score,
                "comment": f"{rating}: {reason}"
            }
            
        except Exception as e:
            print(f"Evaluation error: {e}")
            return {
                "key": "m4_quality",
                "score": 0.0,
                "comment": f"Error: {str(e)}"
            }
    
    return evaluate_m4_quality

def upload_m4_results_to_langsmith():
    """
    Upload M4 test results to LangSmith as a dataset.
    This allows running LLM-as-judge evaluation in the UI.
    """
    
    print("=" * 70)
    print("UPLOADING M4 RESULTS TO LANGSMITH")
    print("=" * 70)
    
    client = Client()
    dataset_name = "financial-planning-milestone4"
    
    # Check if dataset exists
    try:
        existing = client.read_dataset(dataset_name=dataset_name)
        print(f"\nDataset '{dataset_name}' already exists.")
        response = input("Delete and recreate? (yes/no): ")
        
        if response.lower() == 'yes':
            client.delete_dataset(dataset_name=dataset_name)
            print("Deleted existing dataset")
        else:
            print("Using existing dataset")
            return dataset_name
    except:
        pass
    
    # Load test cases
    from tests.milestone4_dataset import M4_TEST_CASES
    
    print(f"\nCreating dataset: {dataset_name}")
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="End-to-end financial planning scenarios for Milestone 4 evaluation"
    )
    
    print(f"\nUploading {len(M4_TEST_CASES[:5])} test cases...")
    
    for i, test_case in enumerate(M4_TEST_CASES[:5], 1):
        inputs = {
            "user_request": test_case['scenario'],
            "test_id": test_case['id'],
            "complexity": test_case['complexity'],
            "domains": ",".join(test_case['domains'])
        }
        
        outputs = {
            "expected_quality": "good_or_excellent",
            "expected_delegation": True,
            "expected_final_plan": True
        }
        
        client.create_example(
            inputs=inputs,
            outputs=outputs,
            dataset_id=dataset.id
        )
        
        print(f"  [{i}/5] {test_case['id']}")
    
    print("\n" + "=" * 70)
    print("DATASET CREATED")
    print("=" * 70)
    print(f"\nView at: https://smith.langchain.com/")
    print(f"   Dataset: {dataset_name}")
    print("=" * 70)
    
    return dataset_name

def run_m4_langsmith_evaluation(dataset_name="financial-planning-milestone4"):
    """
    Run LLM-as-a-judge evaluation on M4 results.
    
    This will:
    1. Load the M4 dataset from LangSmith
    2. Run the final agent on each test case
    3. Use LLM judge to score each result
    4. Upload scores to LangSmith
    """
    
    print("=" * 70)
    print("M4 LLM-AS-A-JUDGE EVALUATION")
    print("=" * 70)
    
    client = Client()
    
    # Check dataset
    try:
        dataset = client.read_dataset(dataset_name=dataset_name)
        print(f"Found dataset: {dataset_name}")
        examples = list(client.list_examples(dataset_id=dataset.id))
        print(f"   Examples: {len(examples)}")
    except Exception as e:
        print(f"Dataset not found: {dataset_name}")
        print(f"\nCreating dataset first...")
        dataset_name = upload_m4_results_to_langsmith()
        dataset = client.read_dataset(dataset_name=dataset_name)
    
    # Load final agent
    print("\nLoading M4 agent...")
    from agents.agent_m4 import agent_m4
    from state.agent_state import create_initial_state
    
    def run_agent(inputs):
        state = create_initial_state(
            inputs["user_request"],
            max_iterations=3   # 🔥 match real agent
        )

        try:
            state = create_initial_state(
                inputs["user_request"],
                max_iterations=3
            )

            result = agent_m4.invoke(state)

            return {
                "files": {
                    "final_financial_plan.txt":
                    result.get("files", {}).get("final_financial_plan.txt", "")
                }
            }

        except Exception as e:
            print(f"Agent failed: {e}")
            return {"files": {}}

        # ONLY RETURN FINAL FILE
        return {
            "files": {
                "final_financial_plan.txt":
                result.get("files", {}).get("final_financial_plan.txt", "")
            }
        }
    
    # Create evaluator
    print("Creating LLM judge (using llama3-8b to save tokens)...")
    evaluator = create_m4_evaluator()
    
    print("\nRunning evaluation...")
    print("This will:")
    print("  1. Run M4 agent on all test cases")
    print("  2. Judge each output with LLM")
    print("  3. Upload results to LangSmith")
    print(f"\nEstimated time: ~10-15 minutes\n")
    
    try:
        results = evaluate(
            run_agent,
            data=dataset_name,
            evaluators=[evaluator],
            experiment_prefix="m4-llm-judge",
            description="LLM-as-a-judge evaluation of complete M4 system",
            max_concurrency=1
        )
        
        print("\n" + "=" * 70)
        print("EVALUATION COMPLETE")
        print("=" * 70)
        
        # Try to get aggregate stats
        try:
            import pandas as pd
            df = results.to_pandas()
            
            if 'm4_quality' in df.columns:
                avg_score = df['m4_quality'].mean()
                excellent_count = sum(df['m4_quality'] >= 0.8)
                good_count = sum((df['m4_quality'] >= 0.6) & (df['m4_quality'] < 0.8))
                
                print(f"\nRESULTS:")
                print(f"   Average Score: {avg_score:.2f}/1.0 ({avg_score*100:.0f}%)")
                print(f"   Excellent: {excellent_count}/{len(df)}")
                print(f"   Good: {good_count}/{len(df)}")
                print(f"   Success Rate: {(excellent_count + good_count)}/{len(df)} ({(excellent_count + good_count)/len(df)*100:.0f}%)")
        except Exception as e:
            print(f"Could not calculate aggregate stats: {e}")
        
        print(f"\nView detailed results:")
        print(f"   https://smith.langchain.com/")
        print(f"   Navigate to: Datasets → {dataset_name} → Experiments")
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
        
        print("\nChoose an option:")
        print("   1. Upload M4 dataset to LangSmith (required first time)")
        print("   2. Run LLM-as-judge evaluation")
        print("   3. Both (recommended)\n")
        
        choice = input("Enter choice (1/2/3): ").strip()
        
        if choice == "1":
            upload_m4_results_to_langsmith()
        elif choice == "2":
            run_m4_langsmith_evaluation()
        else:  # Default to both
            print("\nRunning complete evaluation workflow...\n")
            dataset_name = upload_m4_results_to_langsmith()
            print("\nWaiting 10s before starting evaluation...")
            import time
            time.sleep(10)
            run_m4_langsmith_evaluation(dataset_name)
            
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()