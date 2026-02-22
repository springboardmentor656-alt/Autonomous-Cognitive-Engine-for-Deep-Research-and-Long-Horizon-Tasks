# Autonomous-Cognitive-Engine-for-Deep-Research-and-Long-Horizon-Tasks
PROJECT OVERVIEW

This project implements an Autonomous Multi-Agent Research System capable of handling complex, long-horizon research tasks with minimal human intervention.

Instead of simple question-answering, this system:

Understands a complex research prompt

Breaks it into structured sub-tasks

Executes each task step-by-step

Stores intermediate outputs in memory

Synthesizes a final professional report

Evaluates its own performance

The architecture simulates how a human researcher works end-to-end.

Project Objectives

Build a multi-step autonomous cognitive agent

Implement planning + orchestration + execution workflow

Enable file-based working memory (Virtual File System)

Support long-form report generation

Integrate LLM-as-a-Judge evaluation

Log experiments using LangSmith

🏗️ System Architecture

The system is built using a LangGraph-style cognitive workflow with modular components.

🧩 Core Components
1️⃣ Planning Node (Strategic Thinking)

Receives user input

Breaks the research prompt into 4–6 structured tasks

Stores tasks inside state["todos"]

state["todos"] = todos

👉 Converts vague prompts into actionable research steps.

2️⃣ Orchestrator Node (Control Flow Brain)

Checks if tasks are remaining

Sends next task to worker

Moves to synthesis when all tasks are complete

if state["todos"]:
    return {"next": "execute"}
else:
    return {"next": "synthesize"}

👉 Controls the entire execution loop.

3️⃣ Worker Node (Execution Engine)

Picks one task at a time

Executes it using LLM

Stores output in memory

next_task = state["todos"].pop(0)
state["files"][filename] = result

👉 Simulates research step execution.

4️⃣ Virtual File System (Memory Layer)

Stores:

Research notes

Intermediate summaries

Final report

state["files"][filename] = content

👉 Enables long-horizon reasoning across steps.

5️⃣ Synthesis Node (Final Report Generator)

Combines all stored research outputs

Generates a structured 1200+ word professional report

Saves as final_report.txt

state["files"]["final_report.txt"] = final_report

👉 Produces the final deliverable.

6️⃣ LLM-as-a-Judge (Evaluation System)

Instead of external APIs like Gemini, this project uses:

🦙 Local LLaMA model via Ollama

judge_llm = ChatOllama(model="llama3", temperature=0)

The evaluator:

Grades the report from 1–10

Returns a numeric score

Logs results in LangSmith

Advantages:

✅ No API cost

✅ Offline execution

✅ Reproducible scoring

✅ No dependency on external API keys

🔄 Complete Workflow (Input → Output)

User prompt is received

Planning node generates structured research steps

Orchestrator controls task execution loop

Worker executes each task

Outputs are stored in Virtual File System

Synthesis node generates final report

Final report returned to LangSmith

LLaMA evaluator assigns score (1–10)

This creates a fully autonomous research pipeline.

📂 Project Structure
.
├── agent/
│   ├── planning_node.py
│   ├── orchestrator_node.py
│   ├── worker_node.py
│   ├── synthesis_node.py
│   ├── state.py
│   └── graph.py
│
├── tools/
│   ├── vfs.py
│   ├── write_todos.py
│   └── delegation_tool.py
│
├── evaluator.py
├── run_milestone4_experiment.py
├── main.py
└── README.md
📊 Milestone Progression
✅ Milestone 1 – Strategic Planning

Built planner agent

Generated structured TODO list

Basic multi-step reasoning

✅ Milestone 2 – Memory & Tool Integration

Implemented Virtual File System

Enabled file storage & reading

Added task tracking

Integrated LangSmith tracing

✅ Milestone 3 – Long-Horizon Execution

Added orchestrator node

Implemented task delegation

Structured research pipeline

Improved prompt engineering

✅ Milestone 4 – Evaluation & Full Integration

Unified all components in a single StateGraph

Generated complete long-form research reports

Integrated LLaMA-based automated evaluation

Logged full experiments in LangSmith

Measured research quality with 1–10 scoring scale

📊 Evaluation Results

Average score across tasks: ~7–8 / 10

High task completion rate

Structured and coherent outputs

Stable multi-step execution

The system demonstrates reliable autonomous research capability.

🛠️ Technologies Used

Python

LangChain

LangGraph-style workflow

Ollama (Local LLaMA)

LangSmith (Tracing & Experiments)

Virtual File System memory design

💡 Key Features

✔ Multi-agent cognitive architecture
✔ Autonomous task planning
✔ Loop-based execution control
✔ Long-form research synthesis
✔ Local LLaMA evaluation
✔ LangSmith experiment tracking
✔ Cost-free offline grading

🎓 Learning Outcomes

This project demonstrates:

Multi-agent system design

Long-horizon reasoning architecture

Prompt engineering for complex tasks

LLM-based evaluation methods

Tool-driven agent workflows

Experiment tracking & debugging with LangSmith

🚀 Final Outcome

Milestone 4 successfully delivers:

A fully autonomous research engine capable of planning, executing, synthesizing, and evaluating complex research tasks end-to-end.
