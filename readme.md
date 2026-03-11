# Autonomous Cognitive Engine for Deep Research and Long-Horizon Tasks

A sophisticated AI agent framework built with LangGraph that enables autonomous execution of complex, multi-step tasks through intelligent planning, context management, and specialized sub-agent delegation.

## Project Objectives

This framework implements advanced agent patterns that go beyond simple tool-calling loops to enable:

- **Structured Task Planning**: Dynamic TODO list decomposition and tracking
- **Context Management**: Virtual file system for handling large-scale information
- **Modular Sub-Agents**: Specialized agents with focused contexts and toolsets
- **Stateful Architecture**: LangGraph-based orchestration with robust state management
- **Complex Use Cases**: Autonomous research, multi-step analysis, and long-horizon tasks

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SUPERVISOR AGENT                         │
│                   (LangGraph StateGraph)                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│  │ Planning │───▶│Execution │───▶│Synthesis │            │
│  │   Node   │    │   Node   │    │   Node   │            │
│  └──────────┘    └──────────┘    └──────────┘            │
│                        │                                    │
│                        ▼                                    │
│              ┌──────────────────┐                          │
│              │ Delegation Logic │                          │
│              └────────┬─────────┘                          │
│                       │                                     │
│         ┌─────────────┴─────────────┐                     │
│         ▼                           ▼                      │
│  ┌──────────────┐          ┌──────────────┐              │
│  │ Summarization│          │   Research   │              │
│  │   Sub-Agent  │          │  Sub-Agent   │              │
│  │ (LangGraph)  │          │     (LLM)    │              │
│  └──────────────┘          └──────────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
            │                                │
            ▼                                ▼
    ┌──────────────┐                ┌──────────────┐
    │Virtual File  │                │   LangSmith  │
    │   System     │                │   Tracing    │
    └──────────────┘                └──────────────┘
```

## Key Features

### Milestone 1: Foundational Agent & Task Planning
- ReAct agent loop with LangGraph StateGraph
- AI-powered `write_todos` planning tool
- Automatic task decomposition into 6 sequential steps
- LangSmith tracing integration

### Milestone 2: Context Offloading via Virtual File System
- Virtual file system tools: `ls`, `read_file`, `write_file`, `edit_file`
- State-based file storage (no disk I/O during execution)
- Intermediate result persistence across execution steps
- Context linking between TODO steps

### Milestone 3: Sub-Agent Delegation
- Task delegation tool with sub-agent registry
- **Summarization Agent**: LangGraph-based specialized summarizer
- **Research Agent**: LLM-backed research assistant
- Intelligent routing with heuristic + LLM decision-making
- Delegation tracking in execution logs

### Milestone 4: Full Integration & Use Case
- Complete LangGraph StateGraph architecture
- Enhanced system prompts for all components
- Autonomous research use case implementation
- Manual testing and validation
- LangSmith tracing for all executions

## Quick Start

### Prerequisites

- Python 3.11+
- API keys:
  - Nebius API key (for LLM access)
  - LangChain API key (for LangSmith tracing)

### Installation

1. **Clone the repository**
   ```bash
   cd autonomous_cognitive_engine
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy example env file
   copy .env.example .env  # Windows
   # cp .env.example .env  # Linux/Mac
   
   # Edit .env and add your API keys
   NEBIUS_API_KEY=your_key_here
   LANGCHAIN_API_KEY=your_key_here
   ```

### Usage

#### Interactive Mode
```bash
python main.py
```

#### Command Line Mode
```bash
python main.py "Research the benefits of microservices architecture and summarize key findings"
```

#### Test the System
```bash
python test_system.py
```

## Testing & Validation

The system has been tested and validated through:

### Manual Testing
- Complex multi-step tasks
- Delegation to specialized sub-agents
- Context management via virtual file system
- LangSmith tracing for all executions

### Test Cases
Test with various task types:
- Research tasks (triggers researcher sub-agent)
- Summarization tasks (triggers summarization sub-agent)
- Complex multi-step workflows
- Comparative analysis tasks

### Evaluation Suite
Run end-to-end evaluation with completion and quality metrics:
```bash
python evaluation_suite.py --tasks 10
python evaluation_suite.py --tasks 10 --judge
```
Reports are stored in `output/evaluations/`.

## Tech Stack

- **LangGraph**: Stateful agent orchestration
- **LangChain**: LLM integration and tool creation
- **LangSmith**: Observability and tracing
- **OpenAI-compatible API**: LLM provider (Nebius)
- **Python 3.11+**: Core language

## Project Structure

```
autonomous_cognitive_engine/
├── agent/
│   ├── supervisor.py          # Main supervisor agent with LangGraph
│   └── subagents/
│       ├── researcher.py       # Research sub-agent
│       └── summarizer.py       # Summarization sub-agent (LangGraph)
├── tools/
│   ├── planning.py            # write_todos planning tool
│   ├── filesystem.py          # Virtual file system tools
│   └── delegation.py          # Sub-agent delegation tool
├── use_cases/
│   └── autonomous_research.py # Research use case definitions
├── main.py                    # Main entry point
├── test_system.py             # System verification tests
├── evaluation_suite.py        # [Future] Automated evaluation framework
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Example Tasks

The system excels at complex, multi-step tasks such as:

1. **Research & Analysis**
   - "Research and compare microservices vs monolithic architecture"
   - "Investigate quantum computing applications in cryptography"

2. **Summarization**
   - "Summarize the key principles of circular economy"
   - "Analyze and summarize effective remote work policies"

3. **Multi-Step Planning**
   - "Develop a strategic plan for implementing AI ethics guidelines"
   - "Create a comprehensive analysis of renewable energy adoption"

## LangSmith Tracing

All executions are traced in LangSmith for debugging and analysis:

- Project: `autonomous-cognitive-engine` (interactive)
- Project: `autonomous-cognitive-engine-eval` (evaluation)

View traces at: https://smith.langchain.com/

## Milestones Progress

| Milestone | Status | Description |
|-----------|--------|-------------|
| Milestone 1 | Complete | Foundational agent & task planning |
| Milestone 2 | Complete | Context offloading via virtual file system |
| Milestone 3 | Complete | Sub-agent delegation |
| Milestone 4 | Complete | Full integration, autonomous use case, and end-to-end evaluation |

## Contributing

This is an educational project developed as part of the Infosys Springboard program.

## Acknowledgments

- Built following LangGraph best practices for agent architectures
- Inspired by advanced agent patterns in leading AI systems
- Developed for Infosys Springboard program

---