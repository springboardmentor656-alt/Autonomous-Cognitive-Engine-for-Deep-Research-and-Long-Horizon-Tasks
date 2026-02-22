# Autonomous-Cognitive-Engine-for-Deep-Research-and-Long-Horizon-Tasks
### 📌 Project Overview

This project implements an Autonomous AI Research Agent capable of planning, executing, and generating long-form research outputs with minimal human intervention.

The system simulates how a human researcher works:

Understand the task

Break it into sub-steps

Gather information

Execute the plan

Produce a structured research report

The goal is to build an AI system that can handle complex, multi-step reasoning tasks rather than simple question-answering.

### 🎯 Project Objectives

Build a multi-agent cognitive system for deep research tasks

Implement planning, execution, summarization, and report generation

Enable file-based memory and task tracking

Evaluate the agent’s performance on real research prompts

Measure task completion and output quality

### 🏗️ System Architecture

The project follows a modular cognitive-agent design.

##### 🧩 Core Components
##### 1️⃣ Planner Agent

Breaks user requests into structured steps

Generates an actionable research plan

Stores tasks in memory

##### 2️⃣ Execution Agent

Performs each step of the plan

Uses tools like summarization and file reading

Updates the working state

##### 3️⃣ Summarization Agent

Converts gathered information into structured text

Produces coherent research content

##### 4️⃣ Final Answer Generator

Combines all outputs

Produces a full research report

##### 5️⃣ File System Memory

Saves notes, summaries, and todo lists

Allows long-horizon reasoning across steps

### 🧠 Agent Workflow

User submits a research prompt

Planner generates step-by-step plan

System reads existing notes/files

Execution agent performs tasks

Summaries are generated

Final research report is produced

#### 📂 Project Structure
agent/                  # Core agent logic
tools/                  # Utility tools (file IO, summarization, tasks)
main.py                 # Entry point to run the agent
run_milestone2_experiment.py   # Evaluation runner script
milestone4/             # Evaluation results and documentation
README.md

### 📊 Milestone Implementation
##### ✅ Milestone 1 – Basic Agent Setup

Implemented initial cognitive workflow

Built planner, execution, and summarization agents

Enabled report generation

##### ✅ Milestone 2 – Tool Integration

Added file-based memory system

Implemented todo tracking

Enabled multi-step task execution

Added LangSmith tracing for debugging

##### ✅ Milestone 3 – Long-Horizon Task Support

Improved planning logic

Enhanced execution pipeline

Added structured report generation

Improved prompt design

##### ✅ Milestone 4 – Evaluation & Performance Analysis
###### 🎯 Goal

Evaluate whether the agent can:

Complete end-to-end research tasks

Produce useful and structured outputs

### 🛠️ Evaluation Method

The agent was tested on multiple research prompts representing real-world tasks.

Evaluation metrics:

Task Completion Rate

Whether the agent finishes the task without errors

Output Quality

Judged using an LLM-as-a-Judge approach

### 🤖 LLM-Based Evaluation

Instead of Gemini API, this project uses:

Local LLaMA model via Ollama

This allows:

Offline evaluation

No API cost

Reproducible scoring

The judge model assigns a score from 1 to 10 based on:

Completeness

Clarity

Structure

Usefulness

### 📊 Results Summary

Average score across tasks: ~7+

Most tasks successfully completed

Outputs structured and coherent

System demonstrates reliable research-generation ability

### 🔍 Technologies Used

Python

LangChain

LangGraph-style agent design

Ollama (Local LLaMA model)

LangSmith (Tracing & evaluation)

File-based memory system

### 💡 Key Features

✔ Autonomous multi-step reasoning
✔ File-based persistent memory
✔ Tool-driven execution
✔ Long-form research generation
✔ Local LLM evaluation support
✔ LangSmith tracing integration

### 🎓 Learning Outcomes

Through this project, we demonstrated:

Multi-agent system design

Prompt engineering for long-horizon tasks

LLM-based evaluation methods

Research automation workflow design

Debugging with LangSmith traces
