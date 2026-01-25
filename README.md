# Autonomous-Cognitive-Engine-for-Deep-Research-and-Long-Horizon-Tasks
# Milestone 2: Context Offloading via Virtual File System

## 📋 Overview

This project implements a LangGraph-based AI agent with a **virtual file system** that enables context offloading for multi-step tasks. The agent can save intermediate results to files, retrieve them later, and manage information across complex workflows that exceed typical context windows.

**Project Duration:** Weeks 3-4  
**Framework:** LangGraph, LangChain, Groq  
**Language Model:** Llama 3.3 70B (via Groq)

---

## 🎯 Project Goals

### Primary Objectives
1. ✅ Implement virtual file system tools: `ls`, `read_file`, `write_file`, `edit_file`
2. ✅ Integrate file system into agent's workflow
3. ✅ Enable context offloading for long/multi-step tasks
4. ✅ Achieve >80% success rate on multi-step test scenarios

### Key Features
- **Virtual File System**: In-memory file storage using Python dictionary
- **Context Offloading**: Agent saves intermediate results to avoid context overflow
- **Multi-Step Execution**: Handles tasks requiring sequential processing
- **LangSmith Integration**: Full observability and tracing
- **Automated Evaluation**: 5 comprehensive test scenarios

---

## 📁 Project Structure

```
milestone2_context_offloading/
│
├── .env                          # Environment variables (API keys)
├── .gitignore                    # Git ignore file
├── requirements.txt              # Python dependencies
├── README.md                     # This file
│
├── src/
│   ├── __init__.py
│   ├── state.py                  # AgentState definition with file system
│   ├── tools.py                  # Virtual file system tools
│   └── graph.py                  # LangGraph workflow implementation
│
├── tests/
│   ├── __init__.py
│   ├── test_scenarios.py         # 5 evaluation test cases
│   └── evaluate.py               # Automated evaluation script
│
├── examples/
│   └── interactive_demo.py       # Interactive CLI for testing
│
└── results/
    ├── files/                    # Saved virtual files (per test)
    └── evaluation_summary.txt    # Latest evaluation results
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key (free at https://console.groq.com/)
- LangSmith API Key (optional, for tracing)

### Installation

```bash
# 1. Clone/navigate to project directory
cd milestone2_context_offloading

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
# Create .env file with:
GROQ_API_KEY=your-groq-api-key-here

# Optional - for LangSmith tracing:
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key-here
LANGCHAIN_PROJECT=milestone2-agent
```

### Run Evaluation

```bash
python tests/evaluate.py
```

### Interactive Demo

```bash
python examples/interactive_demo.py
```

---

## 🔧 Virtual File System Tools

### 1. `ls()` - List Files
Lists all files in the virtual file system.

```python
ls()
# Returns: "📁 Files in system (3 total): • file1.txt • file2.txt • file3.txt"
```

### 2. `read_file(filename)` - Read File
Reads content from a specific file.

```python
read_file("notes.txt")
# Returns: "📄 Content of 'notes.txt': This is my note..."
```

### 3. `write_file(filename, content)` - Create/Overwrite File
Creates a new file or overwrites existing one.

```python
write_file("summary.txt", "This is a summary...")
# Returns: "✅ Successfully wrote 25 characters to 'summary.txt'"
```

### 4. `edit_file(filename, new_content)` - Edit Existing File
Modifies an existing file (must exist first).

```python
edit_file("summary.txt", "Updated summary...")
# Returns: "✅ Successfully edited 'summary.txt' (was 25 chars, now 30 chars)"
```

---

## 📊 Evaluation Metrics

### Test Scenarios

| # | Scenario | Description | Expected Files |
|---|----------|-------------|----------------|
| 1 | Multi-Article Summarization | Process 3 articles, create summaries, combine | 4 files |
| 2 | Step-by-Step Research | Research 5 topics, save each, synthesize | 6 files |
| 3 | Iterative Document Creation | Create document through multiple versions | 4 files |
| 4 | Long Context Processing | Analyze customer feedback by category | 5 files |
| 5 | Multi-Step Data Processing | Process sales data, create analyses | 6 files |

### Success Criteria
- ✅ Agent uses `write_file` to save intermediate results: **>80% of scenarios**
- ✅ Agent uses `read_file` to retrieve saved data: **>80% of scenarios**
- ✅ Multi-step tasks completed successfully: **>80% of scenarios**
- ✅ State updates show file content in LangSmith traces

### Expected Results

```
======================================================================
📊 RESULTS SUMMARY
======================================================================

Test                                Status     Files    Writes
----------------------------------------------------------------------
Multi-Article Summarization         ✅ PASS     4        4
Step-by-Step Research               ✅ PASS     6        6
Iterative Document Creation         ✅ PASS     4        4
Long Context Processing             ✅ PASS     5        5
Multi-Step Data Processing          ✅ PASS     6        6

----------------------------------------------------------------------
Total: 5 | Passed: 5 | Failed: 0 | Rate: 100%
----------------------------------------------------------------------

🎉 MILESTONE 2: PASSED
   Success rate 100% meets requirement (>80%)
```

---

## 🎮 Usage Examples

### Example 1: Simple File Creation

```bash
python examples/interactive_demo.py
```

```
You: Create a file called notes.txt with content "Meeting at 3pm"

Agent: I'll create that file for you.
[Executes: write_file("notes.txt", "Meeting at 3pm")]

You: files

📁 VIRTUAL FILE SYSTEM
────────────────────────────────────────
Total files: 1

📄 notes.txt
   Size: 14 characters
   Preview: Meeting at 3pm
```

### Example 2: Multi-Step Task

```
You: Analyze 3 products:
- Product A: $100, 5 stars
- Product B: $150, 4 stars  
- Product C: $200, 5 stars

Create a summary for each, then a comparison report.

Agent: [Processes each product separately]
- Creates product_a.txt
- Creates product_b.txt
- Creates product_c.txt
- Uses ls() to verify
- Creates comparison.txt
```

### Example 3: Context Offloading

```
You: [Provides 3 long articles, 2000+ chars each]
Summarize each article and create a combined analysis.

Agent: [Saves each summary to avoid context overflow]
- Processes Article 1 → write_file("summary1.txt")
- Processes Article 2 → write_file("summary2.txt")
- Processes Article 3 → write_file("summary3.txt")
- Reads all summaries → read_file() × 3
- Creates final → write_file("final_report.txt")
```

---

## 🔍 LangSmith Tracing

### Setup

1. Create account at https://smith.langchain.com/
2. Get API key from Settings → API Keys
3. Add to `.env`:
```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_your-key-here
LANGCHAIN_PROJECT=milestone2-agent
```

### View Traces

1. Run evaluation: `python tests/evaluate.py`
2. Open https://smith.langchain.com/
3. Navigate to project: "milestone2-agent"
4. Click on any run to see detailed trace

### What You'll See

```
Run: Multi-Article Summarization
├── Agent Call #1
│   └── Tool: write_file("summary1.txt", "...")
├── Agent Call #2
│   └── Tool: write_file("summary2.txt", "...")
├── Agent Call #3
│   └── Tool: write_file("summary3.txt", "...")
├── Agent Call #4
│   └── Tool: ls()
├── Agent Call #5-7
│   └── Tools: read_file() × 3
└── Agent Call #8
    └── Tool: write_file("final.txt", "...")
```

---

## 🧪 Testing

### Run All Tests
```bash
python tests/evaluate.py
```

### Run Single Test
```python
# Create test_single.py
from src.graph import create_agent_graph, run_agent
from src.state import AgentState

graph = create_agent_graph()
state = AgentState(messages=[], files={}, intermediate_steps=[])

test = """
Create 3 files:
1. file1.txt with "Content 1"
2. file2.txt with "Content 2"
3. file3.txt with "Content 3"
"""

final_state = run_agent(graph, test, state)
print(f"Files created: {len(final_state['files'])}")
```

```bash
python test_single.py
```

### Interactive Testing
```bash
python examples/interactive_demo.py

# Commands:
# - Type your request
# - 'files' - View all files
# - 'save' - Export files to disk
# - 'reset' - Clear everything
# - 'exit' - Quit
```

---

## 📦 Dependencies

```txt
langchain>=0.1.0
langchain-groq>=0.1.0
langgraph>=0.2.0
langchain-core>=0.1.0
langsmith>=0.1.0
python-dotenv>=1.0.0
typing-extensions>=4.5.0
```

---

## 🐛 Troubleshooting

### Issue: "GROQ_API_KEY not found"

**Solution:**
```bash
# Check .env file exists
cat .env  # Linux/Mac
type .env  # Windows

# Should contain:
GROQ_API_KEY=your-key-here
```

### Issue: "Model decommissioned error"

**Solution:** Update `src/graph.py`, line ~27:
```python
model="llama-3.3-70b-versatile"  # Use this, not llama-3.1
```

### Issue: "No files created"

**Solution:** Check that agent is receiving step-by-step instructions:
```python
# Good ✅
"Create 3 files. Do them ONE AT A TIME:
1. Create file1.txt
2. Create file2.txt
3. Create file3.txt"

# Bad ❌
"Create files file1, file2, file3"
```

### Issue: "LangSmith traces not appearing"

**Solution:**
```bash
# Restart terminal after adding to .env
deactivate
venv\Scripts\activate

# Or set manually:
export LANGCHAIN_TRACING_V2=true  # Linux/Mac
set LANGCHAIN_TRACING_V2=true     # Windows
```

---

## 📈 Performance Metrics

### Current Results (Latest Run)

- **Success Rate:** 60-100% (varies by test complexity)
- **Files Created:** 15-25 across all tests
- **Tool Usage:** 15-30 write_file calls
- **Average Runtime:** 2-5 minutes for full evaluation

### Optimization Tips

1. **Improve Prompts**: Use explicit step-by-step instructions
2. **Increase Recursion**: Set `recursion_limit=100` in graph.py
3. **Simplify Tasks**: Break complex tests into smaller subtests
4. **Better Parsing**: Enhance tool call extraction in graph.py

---

## 🎓 Learning Outcomes

By completing this milestone, you will understand:

1. ✅ **Context Management**: How to offload information to avoid context limits
2. ✅ **LangGraph Architecture**: Building stateful, multi-step workflows
3. ✅ **Tool Integration**: Creating and integrating custom tools
4. ✅ **Agent Evaluation**: Designing and running systematic tests
5. ✅ **Observability**: Using LangSmith for debugging and analysis

---

## 📚 Documentation

- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **LangChain Tools**: https://python.langchain.com/docs/modules/tools/
- **Groq API**: https://console.groq.com/docs/
- **LangSmith**: https://docs.smith.langchain.com/

---

## 🤝 Contributing

This is an educational project for Infosys Internship. For questions or improvements:

1. Document issues in evaluation results
2. Test changes thoroughly
3. Update test scenarios as needed
4. Maintain >80% success rate


---

## 👤 Author

**Intern Name:** Tejswini Korade  
**Program:** Infosys Springboard  
**Duration:** Weeks 3-4  
**Milestone:** 2 - Context Offloading via Virtual File System

---

## 🎉 Milestone Completion Checklist

- [ ] All 4 file system tools implemented
- [ ] Virtual file system integrated in state
- [ ] Agent uses tools correctly in workflow
- [ ] 5 test scenarios created
- [ ] Evaluation script running
- [ ] Success rate >80% achieved
- [ ] LangSmith tracing enabled
- [ ] Files saved to disk for inspection
- [ ] Documentation complete
- [ ] README.md created
- [ ] Ready for review! 🚀

---


**Last Updated:** January 2026  
**Status:** ✅ Milestone 2 Complete
