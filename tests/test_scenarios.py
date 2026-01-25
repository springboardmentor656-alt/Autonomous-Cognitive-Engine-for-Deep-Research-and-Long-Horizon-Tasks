"""
Simplified test scenarios that are easier for the agent to follow.
Each test explicitly breaks down the steps.
"""

# Test Scenario 1: Multi-Article Summarization (Simplified)
TEST_1_MULTI_ARTICLE = """You have 3 articles to summarize. Process them ONE AT A TIME.

ARTICLE 1:
Machine learning has revolutionized technology over the past two decades. Modern deep learning approaches can automatically learn features from raw data, leading to breakthroughs in computer vision, natural language processing, and reinforcement learning.

ARTICLE 2:
Neural networks are computational models with interconnected layers. Convolutional Neural Networks (CNNs) excel at image processing, while Recurrent Neural Networks (RNNs) are effective for sequential data like text.

ARTICLE 3:
AI ethics is crucial as systems become more powerful. Key concerns include algorithmic bias, privacy issues, transparency, and AI safety. International cooperation on AI governance is needed.

STEP-BY-STEP INSTRUCTIONS:
1. Create a 2-3 sentence summary of Article 1 → write_file("summary_article1.txt", "your summary")
2. Create a 2-3 sentence summary of Article 2 → write_file("summary_article2.txt", "your summary")
3. Create a 2-3 sentence summary of Article 3 → write_file("summary_article3.txt", "your summary")
4. Verify files created → ls()
5. Read all three files → read_file("summary_article1.txt"), read_file("summary_article2.txt"), read_file("summary_article3.txt")
6. Combine the summaries into a final synthesis → write_file("final_synthesis.txt", "combined summary")
7. Tell me you're done and show the final synthesis

START NOW with Article 1."""

# Test Scenario 2: Step-by-Step Research (Simplified)
TEST_2_RESEARCH = """Research 5 technology topics. Process ONE topic at a time.

TOPICS:
1. Quantum Computing - Uses quantum mechanics for computation
2. Blockchain - Distributed ledger technology
3. Internet of Things - Connected smart devices
4. 5G Networks - Fifth generation mobile networks
5. Edge Computing - Processing data near the source

STEP-BY-STEP INSTRUCTIONS:
1. Create a brief explanation (2 sentences) of Topic 1 → write_file("research_topic1.txt", "explanation")
2. Create a brief explanation (2 sentences) of Topic 2 → write_file("research_topic2.txt", "explanation")
3. Create a brief explanation (2 sentences) of Topic 3 → write_file("research_topic3.txt", "explanation")
4. Create a brief explanation (2 sentences) of Topic 4 → write_file("research_topic4.txt", "explanation")
5. Create a brief explanation (2 sentences) of Topic 5 → write_file("research_topic5.txt", "explanation")
6. Verify all files → ls()
7. Create a final synthesis showing how these technologies work together → write_file("technology_synthesis.txt", "synthesis")

START NOW with Topic 1."""

# Test Scenario 3: Iterative Document Creation (Simplified)
TEST_3_ITERATIVE = """Create a product description through multiple versions.

PRODUCT: SmartHome AI Assistant

STEP-BY-STEP INSTRUCTIONS:
1. Write initial description (2-3 sentences) → write_file("product_v1.txt", "description")
2. Add 3 key features to the description → write_file("product_v2.txt", "description with features")
3. Add pricing info ($299) and specs → write_file("product_v3.txt", "description with features and pricing")
4. Read the latest version → read_file("product_v3.txt")
5. Add executive summary at beginning → write_file("product_final.txt", "complete version with summary")
6. Verify all versions created → ls()

START NOW with the initial description."""

# Test Scenario 4: Long Context Processing (Simplified)
TEST_4_LONG_CONTEXT = """Analyze customer feedback. Process each category separately.

FEEDBACK:
Positive: Customer 2 (5/5), Customer 5 (4/5), Customer 8 (5/5)
Negative: Customer 1 (2/5), Customer 4 (1/5), Customer 7 (1/5)
Neutral: Customer 3 (3.5/5), Customer 6 (3/5)

STEP-BY-STEP INSTRUCTIONS:
1. Analyze positive feedback (1-2 sentences) → write_file("positive_feedback.txt", "analysis")
2. Analyze negative feedback (1-2 sentences) → write_file("negative_feedback.txt", "analysis")
3. Analyze neutral feedback (1-2 sentences) → write_file("neutral_feedback.txt", "analysis")
4. Create statistics: 3 positive, 3 negative, 2 neutral → write_file("statistics.txt", "stats")
5. Verify all files → ls()
6. Create comprehensive report combining all analyses → write_file("feedback_analysis_report.txt", "report")

START NOW with positive feedback."""

# Test Scenario 5: Multi-Step Data Processing (Simplified)
TEST_5_DATA_PROCESSING = """Analyze sales data. Process ONE calculation at a time.

DATA:
Q1: North $450K, South $380K, East $520K, West $410K
Q2: North $490K, South $420K, East $560K, West $450K
Q3: North $510K, South $440K, East $590K, West $470K
Q4: North $550K, South $480K, East $630K, West $510K

STEP-BY-STEP INSTRUCTIONS:
1. Calculate regional totals → write_file("regional_totals.txt", "North: $2000K, South: $1720K, East: $2300K, West: $1840K")
2. Calculate quarterly totals → write_file("quarterly_totals.txt", "Q1: $1760K, Q2: $1920K, Q3: $2010K, Q4: $2170K")
3. Identify top region (East) → write_file("top_region.txt", "East region with $2300K")
4. Note growth trend (increasing each quarter) → write_file("growth_analysis.txt", "Consistent growth each quarter")
5. Verify all analysis files → ls()
6. Create executive summary → write_file("executive_summary.txt", "Key findings from all analyses")

START NOW with regional totals."""

# All test scenarios
ALL_TEST_SCENARIOS = [
    ("Multi-Article Summarization", TEST_1_MULTI_ARTICLE),
    ("Step-by-Step Research", TEST_2_RESEARCH),
    ("Iterative Document Creation", TEST_3_ITERATIVE),
    ("Long Context Processing", TEST_4_LONG_CONTEXT),
    ("Multi-Step Data Processing", TEST_5_DATA_PROCESSING)
]