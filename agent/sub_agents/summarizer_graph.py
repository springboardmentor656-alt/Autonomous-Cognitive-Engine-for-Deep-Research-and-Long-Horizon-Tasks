from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from agent.llm import get_llm

def build_summarizer_graph():
    prompt = ChatPromptTemplate.from_template(
        """
Summarize the following content clearly and concisely:

{task}
"""
    )

    def summarize_node(state):
        llm = get_llm()
        result = llm.invoke(prompt.format(task=state["task"]))
        state["result"] = result.content
        return state

    graph = StateGraph(dict)
    graph.add_node("summarize", summarize_node)
    graph.set_entry_point("summarize")
    graph.add_edge("summarize", END)

    return graph.compile()
