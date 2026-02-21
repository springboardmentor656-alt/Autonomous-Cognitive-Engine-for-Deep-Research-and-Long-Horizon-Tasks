# Finance Agent: Autonomous Cognitive Multi-Agent Engine for Financial Planning System
Finance Agent is a production-grade autonomous system designed for multi-domain financial planning. Built with **LangGraph**, **LangChain**, and **Groq**, the system demonstrates advanced agentic patterns, including hierarchical task decomposition, persistent state management via a virtual file system, and automated evaluation using LLM-as-a-Judge.

The project was developed through a milestone-driven approach, evolving from a single-agent planner into a sophisticated multi-agent architecture capable of complex financial reasoning and specialist delegation.

Check the complete Langraph Trace here: [Financial-Assistant-Demo](https://smith.langchain.com/public/def19d21-f012-4152-ad06-6a39390aff1c/r)

System Capabilities
-------------------

Given a complex financial profile, the Finance Agent performs the following:

1.  **Task Decomposition:** Parses multi-domain requests into a structured, prioritized execution roadmap.
    
2.  **Specialist Delegation:** Routes domain-specific subtasks to expert agents (Debt, Budget, Investment, Tax).
    
3.  **Context Persistence:** Utilizes a Virtual File System (VFS) to maintain intermediate data, ensuring context is preserved across long-running reasoning chains.
    
4.  **Integrated Synthesis:** Aggregates findings into a cohesive, professional-grade master plan.
    
5.  **Automated Validation:** Evaluates output quality against technical rubrics using LLM-as-a-Judge within LangSmith.
    

Architecture
------------

The system is architected as a stateful Directed Acyclic Graph (DAG) to ensure controlled, iterative reasoning.

![45228f12-68da-4fac-8861-ec47ab22271e](https://github.com/user-attachments/assets/9abc117e-6dfb-4339-94a8-f4658ee3a435)

### Core Components

*   **Supervisor Agent:** Acts as the primary orchestrator. Responsible for initial task planning (write\_todos), state monitoring, delegation routing, and final synthesis.
    
*   **Virtual File System (VFS):** Implements write\_file, read\_file, and edit\_file capabilities. This allows the system to overcome LLM context window limitations by persisting data in a structured directory.
    
*   **Delegation Layer:** Features a delegate\_task tool with duplicate prevention logic, ensuring specialists receive clear, isolated instructions.
    
*   **Specialist Sub-Agents:**
    
    *   **Debt Specialist:** Liability management and interest optimization (Avalanche/Snowball).
        
    *   **Budget Analyst:** Cash flow analysis and monthly allocation optimization.
        
    *   **Investment Advisor:** Portfolio growth projections and retirement planning.
        
    *   **Tax Optimizer:** Fiscal strategy and tax-advantaged account recommendations.
        

Performance & Evaluation
------------------------

The system was rigorously validated across four architectural milestones to ensure reliability and accuracy.

### Milestone Success Rates

<img width="641" height="216" alt="image" src="https://github.com/user-attachments/assets/9b420ac2-4538-491a-8773-717e200e268a" />



### Milestone 4 (Full Integration) Metrics

*   **Completion Rate:** 100% (5/5 complex scenarios)
    
*   **Average Output Quality:** 96% (via LLM-as-a-Judge)
    
*   **Reasoning Efficiency:** 3.0 iterations per scenario
    
*   **Resource Utilization:** 2.6 specialists consulted per query
    

## Testing & Observability

### Automated Test Suites

Run milestone-specific tests to verify system integrity:

Bash

    # Milestone 1: Task Planning logic
    python tests/test_milestone1.py
    
    # Milestone 4: End-to-End System Integration
    python tests/test_milestone4.py

### LLM-as-a-Judge (LangSmith)

The system utilizes LangSmith for automated quality assurance. Final outputs are judged on numerical specificity, structural clarity, and practical utility.

Bash

    # Upload experiment data
    python tests/upload_m4_to_langsmith.py
    
    # Run automated evaluation
    python tests/llm_judge_milestone4.py

### Traceability

All agent reasoning steps, tool calls, and state transitions are traceable in LangSmith under the project: [Financial-Assistant-Demo](https://smith.langchain.com/public/def19d21-f012-4152-ad06-6a39390aff1c/r).

* * *

## Installation & Configuration

### Setup

Bash

    git clone <repository-url>
    cd financial-agent
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Environment Variables (.env)

Code snippet

    GROQ_API_KEY=your_groq_key
    LANGCHAIN_API_KEY=your_langsmith_key
    LANGCHAIN_TRACING_V2=true
    
    LLM_MODEL=llama-3.3-70b-versatile
    SUB_AGENT_MODEL=llama3-8b-8192
    
    MAX_ITERATIONS=15

* * *

## Technical Highlights

*   **Stateful Orchestration:** Managed via LangGraph for predictable multi-agent behavior.
    
*   **VFS-Enhanced Memory:** Persistent storage layer enables deep-dive analysis without context loss.
    
*   **Token Optimization:** Hierarchical design allows for high-complexity output on free-tier inference.
    
*   **Production-Ready Evaluation:** Integration with LangSmith for objective, rubric-based scoring.
    

**Finance Agent is not a simple wrapper; it is an autonomous decision-making engine designed for high-fidelity financial planning.**
