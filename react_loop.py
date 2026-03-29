"""
ReAct-style agent runnable for LangGraph.
Milestone-2 (Week-4):

- Plan task
- Generate 3 summaries
- ToolNode writes them to VFS
- ToolNode reads them back
- Produce final combined summary
"""

from agent.state import AgentState
from agent.planner import plan_task

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import uuid

from agent.config import get_model_name, get_api_key


# -------------------------------------------------
# Initialize LLM (Groq)
# -------------------------------------------------
llm = ChatGroq(
    model=get_model_name(),
    api_key=get_api_key(),
    temperature=0.3
)


# -------------------------------------------------
# LangGraph Agent Runnable
# -------------------------------------------------
# -------------------------------------------------
# LangGraph Agent Runnable
# -------------------------------------------------
def agent_runnable(state: AgentState) -> AgentState:
    tasks = state["tasks"]
    messages = state.get("messages", [])

    # Check conversation history to determine current state
    has_written = False
    has_read = False
    read_contents = []

    for msg in messages:
        if isinstance(msg, ToolMessage):
            if msg.name == "write_file":
                has_written = True
            elif msg.name == "read_file":
                has_read = True
                read_contents.append(msg.content)

    tool_calls = []

    # =================================================
    # STATE 3: READ COMPLETE -> SYNTHESIZE FINAL SUMMARY
    # =================================================
    if has_read:
        # We have the content from the files. Synthesize final answer.
        # Synthesize from the gathered read contents
        combined_text = "\n\n".join(read_contents)
        
        prompt = f"""
You have read the following summaries from the file system:

{combined_text}

Please provide a FINAL SYNTHESIZED summary based on these notes.
"""
        response = llm.invoke([HumanMessage(content=prompt)])
        final_summary = response.content

        state["final_output"] = final_summary
        
        # Return complete
        return {
            "messages": [AIMessage(content=final_summary)],
            "final_output": final_summary
        }


    # =================================================
    # STATE 2: WRITTEN -> READ FILES
    # =================================================
    elif has_written:
        # Files are written. Now we must read them back.
        # We assume strict naming convention from Step 1.
        for i in range(1, 4):
            tool_calls.append({
                "name": "read_file",
                "args": {
                    "filename": f"summary_{i}.txt"
                },
                "id": str(uuid.uuid4())
            })
        
        ai_msg = AIMessage(content="Reading files...", tool_calls=tool_calls)
        state["messages"].append(ai_msg)
        return state


    # =================================================
    # STATE 1: START -> GENERATE & WRITE
    # =================================================
    else:
        # Plan task (standard first step)
        # We can just plan for the first task or a combined one, but for now let's just use the tasks directly.
        state["todos"] = []

        # Generate 3 summaries (one for each task)
        for i, task_str in enumerate(tasks, start=1):
            prompt = f"""
You are a research assistant.

Write a concise but informative research summary
about the following task:

{task_str}
"""
            response = llm.invoke([HumanMessage(content=prompt)])
            
            # Create tool call to write this summary
            tool_calls.append({
                "name": "write_file",
                "args": {
                    "filename": f"summary_{i}.txt",
                    "content": response.content
                },
                "id": str(uuid.uuid4())
            })

        ai_msg = AIMessage(content="Generating summaries for 3 tasks and writing to VFS...", tool_calls=tool_calls)
        state["messages"].append(ai_msg)
        return state
