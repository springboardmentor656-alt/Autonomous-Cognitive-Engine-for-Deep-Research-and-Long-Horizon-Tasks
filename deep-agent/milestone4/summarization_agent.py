from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END

llm = ChatOllama(model="tinyllama", temperature=0)

def summarize_node(state):
    text = state["input"]

    prompt = f"Summarize clearly:\n{text}"

    response = llm.invoke([{"role": "user", "content": prompt}])

    return {"output": response.content}

def build_summarization_agent():
    graph = StateGraph(dict)

    graph.add_node("summarize", summarize_node)
    graph.set_entry_point("summarize")
    graph.add_edge("summarize", END)

    return graph.compile()

summarization_agent_app = build_summarization_agent()
