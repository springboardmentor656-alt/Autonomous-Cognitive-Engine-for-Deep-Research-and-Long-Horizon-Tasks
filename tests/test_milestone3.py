"""
Test Milestone 3: Sub-Agent Delegation

This test verifies:
1. Supervisor creates task plans
2. Supervisor identifies tasks needing specialists
3. Delegation to sub-agents works 
4. Results are integrated back 
"""

from glob import glob
import sys
import glob
import os
from pathlib import Path
from unittest import result

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from state.agent_state import create_initial_state
from agents.supervisor_agent import supervisor_agent

def cleanup_old_results():
    """Delete all .txt files created by previous agent runs."""
    files = glob.glob("*.txt")
    for f in files:
        try:
            os.remove(f)
            print(f"Cleaned up: {f}")
        except OSError:
            pass

# Run cleanup before tests start
print("Cleaning environment...")
cleanup_old_results()

print("=" * 70)
print("MILESTONE 3: SUB-AGENT DELEGATION TEST")
print("=" * 70)

settings.validate()

test_query_1 = """
I need comprehensive financial help:

**Debt Situation:**
- Credit Card 1: $12,000 at 24% APR (min payment $360)
- Credit Card 2: $8,000 at 19% APR (min payment $240)
- Student Loan: $35,000 at 6% APR (min payment $350)

**Income & Expenses:**
- Monthly Income: $6,500
- Rent: $1,800
- Food: $600
- Car: $450
- Insurance: $250
- Utilities: $200
- Other: $400

**Goals:**
- Become debt-free as fast as possible
- Build emergency fund
- Start saving for retirement

Can you create a complete financial plan?
"""

print("\nTest Query 1: Complex Debt + Budget Scenario + Investment Advice")
print("Expected: Delegation to BOTH debt_specialist AND budget_analyst AND investment_advisor")
print("\nRunning supervisor agent...\n")

state_1 = create_initial_state(test_query_1, max_iterations=8)
result_1 = supervisor_agent.invoke(state_1)

print("\n" + "=" * 70)
print("TEST 1 RESULTS")
print("=" * 70)

print(f"\nTasks Created: {len(result_1['todos'])}")
if result_1['todos']:
    print("\nTask Plan:")
    for todo in result_1['todos']:
        print(f"  {todo['id']+1}. {todo['description']}")

print(f"\nFiles Created: {len(result_1['files'])}")
if result_1['files']:
    print("\nFiles:")
    for filename in result_1['files'].keys():
        print(f"  • {filename}")

delegation_files = [
    f for f in result_1['files'].keys()
    if any(x in f for x in ["specialist", "analyst", "advisor", "optimizer"])
]
print(f"\nDelegation Evidence: {len(delegation_files)} specialist result files")
for df in delegation_files:
    print(f"  • {df}")

print(f"\nIterations Used: {result_1['iteration_count']}/{result_1['max_iterations']}")
print("\nFINAL PLAN:")
print(result_1.get("final_output", "No final output generated"))


print("\n" + "=" * 70)
print("TEST 2: Debt-Only Scenario")
print("=" * 70)

test_query_2 = """
I have three credit cards:
1. $5,000 at 22% APR
2. $3,000 at 19% APR  
3. $2,000 at 15% APR

I can pay $800/month total. What's the best payoff strategy?
"""

print("\nTest Query 2: Debt-Only")
print("Expected: Delegation to debt_specialist")
print("\nRunning supervisor agent...\n")

state_2 = create_initial_state(test_query_2, max_iterations=8)
result_2 = supervisor_agent.invoke(state_2)

print("\n" + "=" * 70)
print("TEST 2 RESULTS")
print("=" * 70)

print(f"Tasks: {len(result_2['todos'])}")
print(f"Files: {len(result_2['files'])}")

delegation_files_2 = [
    f for f in result_2['files'].keys()
    if any(x in f for x in ["specialist", "analyst", "advisor", "optimizer"])
]
print(f"Delegations: {len(delegation_files_2)}")
for df in delegation_files_2:
    print(f"  • {df}")
print("\nFINAL PLAN:")
print(result_2.get("final_output", "No final output generated"))

print("\n" + "=" * 70)
print("MILESTONE 3 EVALUATION")
print("=" * 70)

def evaluate_m3(result, test_name):
    """Evaluate Milestone 3 success criteria"""
    score = 0
    max_score = 5
    
    print(f"\n{test_name}:")

    if len(result['todos']) >= 3:
        score += 1
        print("Created comprehensive task plan")
    else:
        print("Task plan insufficient")
    
    delegation_evidence = any(
        any(x in f for x in ["specialist", "analyst", "advisor", "optimizer"])
        for f in result['files'].keys()
    )

    if delegation_evidence:
        score += 1
        print("Delegated to sub-agents")
    else:
        print("No delegation detected")
    
    specialist_files = [
        f for f in result['files'].keys()
        if any(x in f for x in ["specialist", "analyst", "advisor", "optimizer"])
    ]
    if len(specialist_files) > 0:
        score += 1
        print(f"Saved {len(specialist_files)} specialist results")
    else:
        print("No specialist results saved")
    
    if specialist_files:
        total_content = sum(len(result['files'][f]) for f in specialist_files)
        if total_content > 200:  
            score += 1
            print("Specialist results are detailed")
        else:
            print("Specialist results are too brief")
    
    if result['iteration_count'] <= result['max_iterations']:
        score += 1
        print("Completed within iteration limit")
    
    print(f"\n  Score: {score}/{max_score} ({score/max_score*100:.0f}%)")
    return score / max_score

eval_1 = evaluate_m3(result_1, "Test 1: Complex Multi-Domain")
eval_2 = evaluate_m3(result_2, "Test 2: Single Domain")

avg_score = (eval_1 + eval_2) / 2
print(f"\nOVERALL MILESTONE 3 SCORE: {avg_score*100:.0f}%")
print(f"{'MILESTONE 3 PASSED!' if avg_score >= 0.8 else ' NEEDS IMPROVEMENT'} (Target: 80%)")

print("\n" + "=" * 70)
print("DELEGATION ANALYSIS")
print("=" * 70)

print("\nTest 1 Delegations:")
for filename, content in result_1['files'].items():
    if any(x in filename for x in ["specialist", "analyst", "advisor", "optimizer"]):
        print(f"\n{filename}:")
        print(f"   Length: {len(content)} characters")
        preview = content[:200] + "..." if len(content) > 200 else content
        print(f"   Preview: {preview}")

print("\n" + "=" * 70)
print("SUCCESS CRITERIA")
print("=" * 70)
print("""
For Milestone 3, the supervisor should:
Create task plans (from M1)
Use file system (from M2)
Identify tasks needing specialist help
Delegate to appropriate sub-agents
Receive and integrate specialist results
Produce comprehensive final plans
Check LangSmith traces to see the full multi-agent collaboration!
""")

print("\nView traces at: https://smith.langchain.com/")
print("=" * 70)