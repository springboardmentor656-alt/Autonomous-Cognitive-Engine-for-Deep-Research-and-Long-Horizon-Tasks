"""
Direct test of sub-agents (without supervisor)

This tests each specialist individually to verify they work.
"""

import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from agents.sub_agents import run_debt_specialist, run_budget_analyst

print("=" * 70)
print("TESTING SUB-AGENTS DIRECTLY")
print("=" * 70)

settings.validate()

print("\n" + "=" * 70)
print("TEST 1: DEBT SPECIALIST")
print("=" * 70)

debt_task = """
Analyze this debt situation and provide a payoff strategy:

- Credit Card A: $12,000 balance, 24% APR, $360 minimum payment
- Credit Card B: $8,000 balance, 19% APR, $240 minimum payment
- Student Loan: $35,000 balance, 6% APR, $350 minimum payment

Client can pay $1,500/month toward debt. What's the optimal strategy?
"""

print(f"\nTask:\n{debt_task}")
print("\nCalling debt_specialist...\n")

try:
    result = run_debt_specialist(debt_task)
    print("DEBT SPECIALIST RESPONSE:")
    print("=" * 70)
    print(result)
    print("=" * 70)
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 70)
print("TEST 2: BUDGET ANALYST")
print("=" * 70)

budget_task = """
Create a budget plan for this situation:

Monthly Income: $6,500

Current Expenses:
- Rent: $1,800
- Food/Groceries: $600
- Car Payment: $450
- Insurance: $250
- Utilities: $200
- Entertainment: $400
- Other: $300

Goals:
- Build emergency fund ($10,000)
- Save for vacation ($3,000)
- Increase retirement savings

Recommend a budget with savings goals.
"""

print(f"\nTask:\n{budget_task}")
print("\nCalling budget_analyst...\n")

try:
    result = run_budget_analyst(budget_task)
    print("BUDGET ANALYST RESPONSE:")
    print("=" * 70)
    print(result)
    print("=" * 70)
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 70)
print("SUB-AGENT TESTING COMPLETE")
print("=" * 70)
print("""
If both specialists returned detailed analysis:
Sub-agents are working correctly
Ready to test full supervisor delegation

Next: Run test_milestone3.py to test the complete system
""")