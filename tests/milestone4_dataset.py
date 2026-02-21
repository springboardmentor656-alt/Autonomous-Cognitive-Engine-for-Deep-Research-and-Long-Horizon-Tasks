
M4_TEST_CASES = [
    {
        "id": "m4_comprehensive_1",
        "complexity": "high",
        "domains": ["debt", "budget", "investment", "emergency"],
        "scenario": """
I'm 32 years old, married with one child (age 3). Here's my situation:

INCOME:
- My salary: $95,000/year
- Spouse salary: $65,000/year
- Total: $160,000/year ($13,333/month gross, ~$10,000 net)

DEBTS:
- Credit Card 1: $15,000 at 22% APR
- Credit Card 2: $8,000 at 19% APR
- Car Loan: $22,000 at 5.5% APR ($450/month)
- Student Loans: $45,000 at 6% APR ($450/month)

EXPENSES:
- Mortgage: $2,200/month
- Utilities: $300/month
- Groceries: $800/month
- Childcare: $1,200/month
- Insurance: $400/month
- Gas/Transport: $300/month
- Other: $500/month

SAVINGS:
- Emergency fund: $5,000
- 401(k): $35,000 (contributing 5%, employer matches 3%)
- No other investments

GOALS:
- Pay off credit card debt ASAP
- Build 6-month emergency fund
- Save for child's college ($50,000 by age 18)
- Retire comfortably at 65
- Buy bigger home in 5 years (need $60,000 down payment)

Create a comprehensive financial plan addressing all goals with specific timelines and monthly allocations.
        """,
        "expected_outputs": {
            "has_debt_strategy": True,
            "has_budget_plan": True,
            "has_emergency_fund_plan": True,
            "has_investment_strategy": True,
            "has_timeline": True,
            "has_specific_numbers": True
        }
    },
    
    {
        "id": "m4_retirement_focused",
        "complexity": "medium",
        "domains": ["investment", "budget", "tax"],
        "scenario": """
I'm 45 years old, single, no kids. I feel behind on retirement:

INCOME: $120,000/year (self-employed consultant)

CURRENT RETIREMENT SAVINGS: Only $80,000 in IRA

EXPENSES: $5,500/month total

CONCERNS:
- Want to retire at 65 (20 years away)
- Need $2 million to maintain lifestyle
- Worried about taxes as self-employed
- Not sure how much to save monthly
- Don't know proper asset allocation for my age

Help me create an aggressive but realistic retirement catch-up plan.
        """,
        "expected_outputs": {
            "has_retirement_calculation": True,
            "has_monthly_savings_target": True,
            "has_investment_allocation": True,
            "has_tax_strategy": True
        }
    },
    
    {
        "id": "m4_debt_crisis",
        "complexity": "high",
        "domains": ["debt", "budget", "emergency"],
        "scenario": """
I'm drowning in debt and need help urgently:

INCOME: $4,800/month (take-home)

DEBTS (total $78,000):
- CC1: $12,000 at 26% APR (min $360)
- CC2: $9,000 at 23% APR (min $270)
- CC3: $7,000 at 21% APR (min $210)
- Personal Loan: $15,000 at 12% APR (min $450)
- Medical Bills: $10,000 (payment plan $200/month)
- Student Loans: $25,000 at 7% APR (min $250)

MUST-PAY EXPENSES: $3,200/month (rent, food, utilities, car)

Current situation: Paying $1,740 in minimum payments, leaving only $860/month for everything else. I'm constantly short and using credit cards for emergencies.

NO SAVINGS. NO EMERGENCY FUND.

I need a realistic plan to get out of this hole. Should I consider debt consolidation? Balance transfer? What should I do FIRST?
        """,
        "expected_outputs": {
            "has_debt_strategy": True,
            "has_consolidation_analysis": True,
            "has_priority_order": True,
            "has_budget_cuts": True,
            "has_timeline": True
        }
    },
    
    {
        "id": "m4_young_professional",
        "complexity": "low",
        "domains": ["budget", "investment", "emergency"],
        "scenario": """
I'm 25, just got my first real job:

INCOME: $75,000/year (~$4,700/month take-home)

NO DEBT (lucky me!)

EXPENSES:
- Rent: $1,500
- Food: $500
- Car: $350
- Insurance: $200
- Fun: $600
- Other: $300

CURRENT SAVINGS: $8,000 in checking (doing nothing)

QUESTIONS:
- How much should I save vs spend?
- Should I max out 401(k)? Roth IRA?
- How much emergency fund?
- Can I afford to buy a car/condo soon?
- What's a good budget for someone my age?

Help me start my financial life on the right foot!
        """,
        "expected_outputs": {
            "has_budget_plan": True,
            "has_retirement_start": True,
            "has_emergency_fund_plan": True,
            "has_priority_guidance": True
        }
    },
    
    {
        "id": "m4_career_transition",
        "complexity": "medium",
        "domains": ["budget", "emergency", "investment"],
        "scenario": """
Major life change - need financial planning:

CURRENT: $110,000/year corporate job (hate it)
NEW OPPORTUNITY: Start own business (expected $60,000/year first year, $90,000 year 2)

SAVINGS: $45,000 emergency fund
401(k): $120,000 (can't contribute if self-employed initially)

DEBTS: Only $15,000 car loan at 4%

EXPENSES: $4,800/month currently, but can cut to $4,000

CONCERNS:
- Can I afford the income drop?
- How long will my savings last?
- Should I keep maxing 401(k) before I quit?
- What's the minimum emergency fund I need?
- When's the safe time to make this jump?

Give me a realistic transition plan with "go/no-go" criteria.
        """,
        "expected_outputs": {
            "has_income_analysis": True,
            "has_runway_calculation": True,
            "has_decision_criteria": True,
            "has_risk_mitigation": True
        }
    }
    
]

def get_m4_tests(count=None, complexity=None):
    """Get M4 test cases with optional filtering"""
    tests = M4_TEST_CASES
    
    if complexity:
        tests = [t for t in tests if t["complexity"] == complexity]
    
    if count:
        tests = tests[:count]
    
    return tests

def print_test_summary():
    """Print summary of M4 test dataset"""
    print("=" * 70)
    print("MILESTONE 4: END-TO-END TEST DATASET")
    print("=" * 70)
    print(f"Total scenarios: {len(M4_TEST_CASES)}")
    
    by_complexity = {}
    by_domain = {}
    
    for test in M4_TEST_CASES:
        comp = test["complexity"]
        by_complexity[comp] = by_complexity.get(comp, 0) + 1
        
        for domain in test["domains"]:
            by_domain[domain] = by_domain.get(domain, 0) + 1
    
    print("\nBy Complexity:")
    for comp, count in sorted(by_complexity.items()):
        print(f"  {comp}: {count}")
    
    print("\nBy Domain:")
    for domain, count in sorted(by_domain.items()):
        print(f"  {domain}: {count}")
    
    print("=" * 70)

if __name__ == "__main__":
    print_test_summary()