"""
Automated evaluation for Milestone 1: Task Planning
This script runs all test cases and evaluates task decomposition quality.
"""

import sys
sys.path.append('..')

from agents.main_agent import financial_agent
from state.agent_state import create_initial_state
from tests.test_dataset import get_test_cases
from typing import List, Dict
import json

def evaluate_task_plan(todos: List[Dict], expected_tasks: List[str]) -> Dict:
    """
    Evaluate the quality of generated task plan.
    
    Criteria:
    1. Has minimum number of tasks (3+)
    2. Tasks are specific and actionable
    3. Tasks are relevant to the request
    """
    
    evaluation = {
        "score": 0.0,
        "total_points": 3,
        "checks": {}
    }
    
    has_enough_tasks = len(todos) >= 3
    evaluation["checks"]["has_enough_tasks"] = has_enough_tasks
    if has_enough_tasks:
        evaluation["score"] += 1
    
    action_verbs = ['calculate', 'analyze', 'gather', 'estimate', 'create', 
                    'develop', 'evaluate', 'assess', 'determine', 'compare', 
                    'review', 'identify', 'build', 'generate', 'project']
    
    specific_count = 0
    for todo in todos:
        desc = todo['description'].lower()
        if any(verb in desc for verb in action_verbs):
            specific_count += 1
    
    specificity_ratio = specific_count / len(todos) if todos else 0
    is_specific = specificity_ratio >= 0.5
    evaluation["checks"]["is_specific"] = is_specific
    evaluation["checks"]["specificity_ratio"] = specificity_ratio
    if is_specific:
        evaluation["score"] += 1
    
    relevance_count = 0
    for expected in expected_tasks:
        for todo in todos:
            if any(word in todo['description'].lower() for word in expected.split()):
                relevance_count += 1
                break
    
    relevance_ratio = relevance_count / len(expected_tasks) if expected_tasks else 0
    is_relevant = relevance_ratio >= 0.5
    evaluation["checks"]["is_relevant"] = is_relevant
    evaluation["checks"]["relevance_ratio"] = relevance_ratio
    if is_relevant:
        evaluation["score"] += 1
    
    evaluation["final_score"] = evaluation["score"] / evaluation["total_points"]
    evaluation["passed"] = evaluation["final_score"] >= 0.67  # 2/3 checks
    
    return evaluation

def run_evaluation(test_count=None):
    """
    Run evaluation on test dataset.
    
    Args:
        test_count: Number of tests to run (None = all)
    """
    test_cases = get_test_cases(test_count)
    results = []
    
    print("=" * 70)
    print("MILESTONE 1 EVALUATION: TASK PLANNING")
    print("=" * 70)
    print(f"Running {len(test_cases)} test cases...\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] Testing: {test_case['category']}")
        
        try:
            state = create_initial_state(test_case['prompt'], max_iterations=5)
            result = financial_agent.invoke(state)
            evaluation = evaluate_task_plan(
                result['todos'], 
                test_case['expected_tasks']
            )
            result_record = {
                "test_id": test_case['id'],
                "category": test_case['category'],
                "todos_generated": len(result['todos']),
                "evaluation": evaluation,
                "todos": [todo['description'] for todo in result['todos']]
            }
            results.append(result_record)
            status = "PASS" if evaluation['passed'] else "FAIL"
            print(f"  {status} | Score: {evaluation['final_score']:.0%} | Tasks: {len(result['todos'])}")
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
            results.append({
                "test_id": test_case['id'],
                "category": test_case['category'],
                "error": str(e)
            })
    passed = sum(1 for r in results if r.get('evaluation', {}).get('passed', False))
    total = len(results)
    success_rate = passed / total if total > 0 else 0
    
    avg_score = sum(r.get('evaluation', {}).get('final_score', 0) for r in results) / total if total > 0 else 0
    
    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)
    print(f"Tests Passed: {passed}/{total} ({success_rate:.0%})")
    print(f"Average Score: {avg_score:.0%}")
    print(f"\nMilestone 1 Target: 80% success rate")
    print(f"Status: {'MILESTONE ACHIEVED' if success_rate >= 0.8 else 'NEEDS IMPROVEMENT'}")
    print("=" * 70)
    
    print("\nDETAILED BREAKDOWN BY CATEGORY:")
    categories = {}
    for r in results:
        cat = r['category']
        if cat not in categories:
            categories[cat] = {'passed': 0, 'total': 0}
        categories[cat]['total'] += 1
        if r.get('evaluation', {}).get('passed', False):
            categories[cat]['passed'] += 1
    
    for cat, stats in sorted(categories.items()):
        rate = stats['passed'] / stats['total'] if stats['total'] > 0 else 0
        print(f"  {cat}: {stats['passed']}/{stats['total']} ({rate:.0%})")
    
    with open('milestone1_results.json', 'w') as f:
        json.dump({
            'summary': {
                'passed': passed,
                'total': total,
                'success_rate': success_rate,
                'average_score': avg_score
            },
            'results': results
        }, f, indent=2)
    
    print(f"\nResults saved to: milestone1_results.json")
    print("\nNext step: Check LangSmith dashboard for detailed traces")
    print("   URL: https://smith.langchain.com/")
    
    return results

if __name__ == "__main__":
    print("Quick evaluation (5 tests)...\n")
    run_evaluation(5)
    
    print("\n" + "=" * 70)
    print("To run full evaluation (10 tests), use:")
    print("  from tests.evaluation import run_evaluation")
    print("  run_evaluation()")
    print("=" * 70)