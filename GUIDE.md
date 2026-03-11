# Autonomous Cognitive Engine - Study Guide

## 1) What this project does
This project runs complex user tasks using a stateful LangGraph supervisor.
It breaks work into TODO steps, executes each step, delegates when useful, and creates a final output.

Core capabilities:
- Structured planning (`write_todos`)
- Context persistence in virtual files (`state["files"]`)
- Sub-agent delegation (`researcher_agent`, `summarization_agent`, `web_search_agent`)
- Final synthesis into one deliverable

## 2) Where execution starts
Start file: `main.py`

Main flow:
1. Load `.env` values.
2. Validate `NEBIUS_API_KEY`.
3. Read user task from CLI argument or input prompt.
4. Call `supervisor_agent(user_task)`.
5. Show generated virtual files.
6. Optionally save all virtual files into `output/`.

## 3) Supervisor architecture
Main orchestrator: `agent/supervisor.py`

Graph nodes:
- `planning_node`
- `execution_node`
- `synthesis_node`

Graph routing:
- Entry: `plan`
- Then `execute`
- Loop in `execute` until all TODOs are done
- End with `synthesize`

State object (`SupervisorState`):
- `input`: original user request
- `todos`: planned steps
- `completed_todos`: completed items
- `current_todo_index`: loop pointer
- `status`: run status
- `files`: virtual file system (all generated artifacts)
- `final_output`: final synthesized response
- `error`: error message if any

## 4) Tool modules and their job
### `tools/planning.py`
- `write_todos(task)`
- Uses LLM to return exactly 6 ordered TODO items.

### `tools/delegation.py`
- `SUBAGENT_REGISTRY`: available sub-agents
- `list_subagents()`: metadata for routing
- `delegate_task(task_input, agent_name)`: execute selected sub-agent

### `tools/filesystem.py`
Virtual file helpers operating on `state["files"]`:
- `ls(state)`
- `write_file(state, filename, content)`
- `read_file(state, filename)`
- `edit_file(state, filename, new_content)`

## 5) Sub-agents
### `agent/subagents/researcher.py`
- `research_agent(question)`
- Returns structured research answer from model.

### `agent/subagents/summarizer.py`
- `summarization_agent(text)`
- Runs its own mini LangGraph (`summarize -> END`) and returns summary.

### `agent/subagents/web_search.py`
- `web_search_agent(query)`
- Runs a lightweight web search and returns top findings.

## 6) Execution flow (end-to-end)
1. User asks a complex task.
2. `planning_node` creates TODO list and saves `todos.txt`.
3. `execution_node` picks one TODO at a time.
4. It builds context from earlier `todo_X_result.txt` files.
5. It decides delegation:
   - search/web/latest/source-like tasks -> `web_search_agent`
   - summarize-like tasks -> `summarization_agent`
   - research-like tasks -> `researcher_agent`
   - else -> direct LLM execution in supervisor
6. It saves each result as `todo_X_result.txt`.
7. After all steps, `synthesis_node` builds:
   - `execution_summary.txt`
   - `final_output.txt`

## 7) Example run
Command:
```bash
python main.py "Research AI agents for education and produce final recommendations"
```

Typical generated files:
- `todos.txt`
- `todo_1_result.txt` ... `todo_6_result.txt`
- `execution_summary.txt`
- `final_output.txt`

## 8) How to read this code quickly
Recommended order:
1. `main.py`
2. `agent/supervisor.py`
3. `tools/planning.py`
4. `tools/delegation.py`
5. `agent/subagents/researcher.py`
6. `agent/subagents/summarizer.py`
7. `tools/filesystem.py`

This order follows runtime flow from entrypoint to orchestration to tools/sub-agents.

## 9) Milestone 4 execution and evaluation
Primary use case runner:
```bash
python use_cases/autonomous_research.py
```

End-to-end evaluation suite (10 tasks):
```bash
python evaluation_suite.py --tasks 10
```

Evaluation with LLM-as-a-judge:
```bash
python evaluation_suite.py --tasks 10 --judge
```

Outputs:
- JSON report is saved in `output/evaluations/`
- Report includes:
   - completion rate
   - good/excellent output rate
   - pass/fail for >70% success criteria
