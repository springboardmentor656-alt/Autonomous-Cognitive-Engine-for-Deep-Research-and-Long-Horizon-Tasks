📖 Overview

Milestone 2 focuses on enhancing the Agentic AI system by enabling it to manage long context using a virtual file system. Instead of relying only on in-memory context, the agent can now store and retrieve intermediate information using file system tools during a single task execution.

🎯 Objective of Milestone 2

Implement a virtual file system inside the agent state

Enable the agent to save intermediate results (e.g., summaries)

Allow the agent to retrieve stored information when needed

Reduce context overload during multi-step task execution

🧠 Key Concepts Used

Context Offloading

Virtual File System

Agent State Management

Multi-step Task Execution

Tool-based Reasoning

🛠️ Technologies Used

Python

LangGraph

LangSmith (Tracing & Debugging)

VS Code

Terminal
Virtual File System Tools

The following tools are implemented and integrated into the agent:

ls – Lists files stored in the virtual file system

write_file – Saves intermediate results (e.g., article summaries)

read_file – Retrieves saved content when needed

edit_file – Updates existing file content

These tools interact with a dictionary stored inside the LangGraph state.

▶️ How the Agent Works

The user provides a single task (e.g., summarize multiple articles)

The agent breaks the task into smaller steps

Intermediate summaries are saved using write_file

Saved data is retrieved using read_file

A final combined summary is generated and displayed 
Evaluation & Verification

Tool Used: LangSmith Tracing

Verified correct usage of:

write_file for saving summaries

read_file for retrieving summaries

State updates and file contents are visible in the trace