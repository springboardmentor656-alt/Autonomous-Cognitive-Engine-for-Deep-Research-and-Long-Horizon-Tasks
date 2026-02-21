import sys
import os
from pathlib import Path
import json
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from state.agent_state import create_initial_state
from agents.agent_m4 import agent_m4
from tests.milestone4_dataset import get_m4_tests

print("=" * 70)
print("MILESTONE 4: END-TO-END SYSTEM EVALUATION")
print("=" * 70)

settings.validate()

def evaluate_output_quality(result, expected_outputs):
    """
    Evaluate the quality of agent output.
    
    Checks for:
    - Completeness (addressed all aspects)
    - Specificity (has numbers, timelines)
    - Actionability (clear next steps)
    - Structure (well-organized)
    """
    score = 0
    max_score = 10
    feedback = []
    
    if len(result['todos']) >= 3:
        score += 2
        feedback.append("Comprehensive task plan")
    else:
        feedback.append("Insufficient task planning")
    
    specialist_files = [f for f in result['files'].keys() 
                       if 'specialist' in f or 'analyst' in f or 'advisor' in f]
    if len(specialist_files) >= 2:
        score += 2
        feedback.append(f"Multi-domain delegation ({len(specialist_files)} specialists)")
    elif len(specialist_files) == 1:
        score += 1
        feedback.append("Limited delegation")
    else:
        feedback.append("No specialist consultation")
    
    has_final = any('final' in f.lower() or 'comprehensive' in f.lower() 
                   for f in result['files'].keys())
    if has_final:
        final_files = [f for f in result['files'].keys() 
                      if 'final' in f.lower() or 'comprehensive' in f.lower()]
        final_content = result['files'][final_files[0]] if final_files else ""
        
        if len(final_content) > 500:
            score += 2
            feedback.append("Comprehensive final plan")
        else:
            score += 1
            feedback.append("Final plan too brief")
    else:
        feedback.append("No final plan generated")
    
    all_content = " ".join(result['files'].values())
    
    has_numbers = any(c.isdigit() for c in all_content)
    has_currency = '$' in all_content or 'dollar' in all_content.lower()
    has_percentages = '%' in all_content
    
    specificity_score = sum([has_numbers, has_currency, has_percentages])
    if specificity_score >= 2:
        score += 2
        feedback.append("Specific with numbers/timelines")
    elif specificity_score == 1:
        score += 1
        feedback.append("Some specificity")
    else:
        feedback.append("Too vague/generic")
    
    total_content_length = sum(len(c) for c in result['files'].values())
    if total_content_length > 3000:
        score += 2
        feedback.append("Detailed and comprehensive")
    elif total_content_length > 1500:
        score += 1
        feedback.append("Adequate detail")
    else:
        feedback.append("Insufficient detail")
    
    return {
        "score": score,
        "max_score": max_score,
        "percentage": (score / max_score) * 100,
        "quality_rating": "excellent" if score >= 8 else "good" if score >= 6 else "acceptable" if score >= 4 else "poor",
        "feedback": feedback
    }

def run_m4_evaluation(test_count=5):    
    test_cases = get_m4_tests(count=test_count)
    results = []
    
    print(f"\nRunning {len(test_cases)} end-to-end scenarios...")
    print(f"This will take several minutes...\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print("=" * 70)
        print(f"TEST {i}/{len(test_cases)}: {test_case['id']}")
        print(f"Complexity: {test_case['complexity']} | Domains: {', '.join(test_case['domains'])}")
        print("=" * 70)
        
        try:
            state = create_initial_state(test_case['scenario'], max_iterations=3)
            result = agent_m4.invoke(state)
            
            quality = evaluate_output_quality(result, test_case.get('expected_outputs', {}))
            
            test_result = {
                "test_id": test_case['id'],
                "complexity": test_case['complexity'],
                "domains": test_case['domains'],
                "completed": True,
                "iterations": result['iteration_count'],
                "todos_created": len(result['todos']),
                "files_created": len(result['files']),
                "delegations": len([f for f in result['files'].keys() 
                                   if 'specialist' in f or 'analyst' in f]),
                "quality": quality,
                "timestamp": datetime.now().isoformat()
            }
            results.append(test_result)
            
            print(f"\nCOMPLETED")
            print(f"Quality: {quality['quality_rating']} ({quality['percentage']:.0f}%)")
            print(f"Tasks: {len(result['todos'])} | Files: {len(result['files'])} | Iterations: {result['iteration_count']}")
            for fb in quality['feedback']:
                print(f"   {fb}")
            
        except Exception as e:
            print(f"\nERROR: {str(e)}")
            results.append({
                "test_id": test_case['id'],
                "completed": False,
                "error": str(e)
            })
    
    return results

def analyze_results(results):
    
    print("\n" + "=" * 70)
    print("MILESTONE 4: FINAL EVALUATION RESULTS")
    print("=" * 70)
    
    completed = [r for r in results if r.get('completed', False)]
    total = len(results)
    
    completion_rate = len(completed) / total if total > 0 else 0
    print(f"\nCompletion Rate: {len(completed)}/{total} ({completion_rate*100:.1f}%)")
    
    if completed:
        quality_counts = {}
        quality_scores = []
        
        for r in completed:
            quality = r['quality']['quality_rating']
            quality_counts[quality] = quality_counts.get(quality, 0) + 1
            quality_scores.append(r['quality']['percentage'])
        
        avg_quality = sum(quality_scores) / len(quality_scores)
        
        print(f"\nQuality Distribution:")
        for rating in ['excellent', 'good', 'acceptable', 'poor']:
            count = quality_counts.get(rating, 0)
            pct = (count / len(completed) * 100) if completed else 0
            print(f"{rating.capitalize()}: {count} ({pct:.1f}%)")
        
        print(f"\nAverage Quality Score: {avg_quality:.1f}%")
        
        success_count = sum(1 for r in completed 
                           if r['quality']['quality_rating'] in ['good', 'excellent'])
        success_rate = success_count / len(completed) if completed else 0
        
        print(f"\nSUCCESS RATE: {success_count}/{len(completed)} ({success_rate*100:.1f}%)")
        print(f"Target: >70%")
        
        if success_rate >= 0.70:
            print(f"\nMILESTONE 4 PASSED!")
        else:
            print(f"\nBelow target - needs improvement")
        
        print(f"\nPerformance Stats:")
        avg_iterations = sum(r['iterations'] for r in completed) / len(completed)
        avg_files = sum(r['files_created'] for r in completed) / len(completed)
        avg_delegations = sum(r['delegations'] for r in completed) / len(completed)
        
        print(f"   Avg Iterations: {avg_iterations:.1f}")
        print(f"   Avg Files: {avg_files:.1f}")
        print(f"   Avg Delegations: {avg_delegations:.1f}")
    
    if completed:
        print(f"\nResults by Complexity:")
        by_complexity = {}
        for r in completed:
            comp = r.get('complexity', 'unknown')
            if comp not in by_complexity:
                by_complexity[comp] = []
            by_complexity[comp].append(r['quality']['percentage'])
        
        for comp, scores in sorted(by_complexity.items()):
            avg = sum(scores) / len(scores)
            print(f"   {comp.capitalize()}: {avg:.1f}% avg ({len(scores)} tests)")
    
    return {
        "completion_rate": completion_rate,
        "success_rate": success_rate if completed else 0,
        "average_quality": avg_quality if completed else 0,
        "passed": success_rate >= 0.70 if completed else False
    }

if __name__ == "__main__":
    print("\nRunning 5 test scenarios (use test_count parameter for more)")
    print("Each test takes ~1-2 minutes")
    print("Full 20-test suite takes ~30-40 minutes\n")
    
    results = run_m4_evaluation(test_count=5)
    
    summary = analyze_results(results)
    
    output_file = f"milestone4_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            "summary": summary,
            "details": results
        }, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    print(f"\nView traces at: https://smith.langchain.com/")
    print("=" * 70)