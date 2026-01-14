"""
Test dataset for evaluating the Financial Planning Agent.
These prompts cover various financial planning scenarios.
"""

MILESTONE_1_TEST_CASES = [
    {
        "id": "retirement_1",
        "category": "Retirement Planning",
        "prompt": """I'm 35 years old, making $80,000/year. I have $50,000 in student loans 
        and $10,000 in credit card debt. I want to retire at 65 with a comfortable lifestyle. 
        Can you help me create a comprehensive financial plan?""",
        "expected_tasks": ["gather financial info", "debt analysis", "retirement calculation", "savings strategy"]
    },
    {
        "id": "emergency_fund_1",
        "category": "Emergency Fund",
        "prompt": """I need to build an emergency fund. I have no savings currently, 
        make $4,000/month, and spend about $3,500/month. How should I approach this?""",
        "expected_tasks": ["expense analysis", "savings goal", "action plan"]
    },
    {
        "id": "investment_1",
        "category": "Investment Strategy",
        "prompt": """I'm 45 years old with $200,000 in my 401(k), all in stocks. 
        I'm worried about market volatility as I approach retirement. Should I rebalance? 
        What's the right asset allocation for my age?""",
        "expected_tasks": ["portfolio analysis", "risk assessment", "allocation recommendation"]
    },
    {
        "id": "debt_payoff_1",
        "category": "Debt Management",
        "prompt": """I have three credit cards with balances: $5,000 at 18% APR, 
        $3,000 at 22% APR, and $2,000 at 15% APR. I can pay $800/month total. 
        What's the best payoff strategy?""",
        "expected_tasks": ["list debts", "calculate interest", "compare methods", "create payoff plan"]
    },
    {
        "id": "home_buying_1",
        "category": "Home Buying",
        "prompt": """My spouse and I make $120,000 combined. We have $40,000 saved 
        and want to buy our first home in 2 years. Homes in our area cost around $350,000. 
        Are we on track? What should we do?""",
        "expected_tasks": ["calculate needed down payment", "assess current savings", "create savings plan"]
    },
    {
        "id": "college_savings_1",
        "category": "Education Planning",
        "prompt": """My child is 5 years old. I want to save for college but don't know 
        where to start. Should I use a 529 plan? How much should I save monthly?""",
        "expected_tasks": ["estimate college costs", "evaluate 529 benefits", "calculate monthly savings"]
    },
    {
        "id": "budget_1",
        "category": "Budgeting",
        "prompt": """I make $5,000/month but always run out of money before the next paycheck. 
        I don't know where it all goes. Can you help me create a budget?""",
        "expected_tasks": ["expense tracking", "categorize spending", "budget creation", "savings goals"]
    },
    {
        "id": "insurance_1",
        "category": "Insurance Planning",
        "prompt": """I'm 30, married with one child. I have no life insurance. 
        Do I need it? How much coverage? What type?""",
        "expected_tasks": ["assess needs", "calculate coverage amount", "compare insurance types"]
    },
    {
        "id": "career_change_1",
        "category": "Career Transition",
        "prompt": """I want to change careers but it means taking a 20% pay cut initially. 
        I make $90,000 now with $15,000 in savings. Can I afford this transition?""",
        "expected_tasks": ["calculate reduced income", "assess expenses", "emergency fund check", "transition plan"]
    },
    {
        "id": "tax_optimization_1",
        "category": "Tax Planning",
        "prompt": """I'm self-employed making $150,000/year. I feel like I'm paying too much in taxes. 
        What strategies can I use to optimize my tax situation?""",
        "expected_tasks": ["review deductions", "retirement account strategy", "business expense optimization"]
    }
]

def get_test_cases(count=None):
    """Get test cases for evaluation"""
    if count:
        return MILESTONE_1_TEST_CASES[:count]
    return MILESTONE_1_TEST_CASES

def print_test_summary():
    """Print summary of test dataset"""
    print("=" * 60)
    print("TEST DATASET SUMMARY")
    print("=" * 60)
    print(f"Total test cases: {len(MILESTONE_1_TEST_CASES)}")
    
    categories = {}
    for case in MILESTONE_1_TEST_CASES:
        cat = case['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nBy category:")
    for cat, count in categories.items():
        print(f"  {cat}: {count}")
    print("=" * 60)

if __name__ == "__main__":
    print_test_summary()