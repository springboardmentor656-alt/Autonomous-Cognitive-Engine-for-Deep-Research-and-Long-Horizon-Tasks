from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

# -------------------------------
# Sub-agent LLM
# -------------------------------
llm = ChatOllama(model="tinyllama")

# -------------------------------
# Sub-agent state
# -------------------------------
def summarize_node(state: dict):
    text = state["input"]

    prompt = f"""
    Summarize the following text clearly and concisely:

    {text}
    """

    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        "output": response.content
    }

# -------------------------------
# Build sub-agent graph
# -------------------------------
def build_summarization_agent():
    graph = StateGraph(dict)

    graph.add_node("summarize", summarize_node)
    graph.set_entry_point("summarize")
    graph.add_edge("summarize", END)

    return graph.compile()


# Export sub-agent app
summarization_agent_app = build_summarization_agent()
