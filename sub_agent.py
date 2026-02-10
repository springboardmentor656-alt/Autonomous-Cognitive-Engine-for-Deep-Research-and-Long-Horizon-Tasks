from langgraph.graph import StateGraph

def summarization_node(state: dict):
    task = state["task"]

    result = (
        "Summary from sub-agent:\n"
        "- Learn AI fundamentals\n"
        "- Master Machine Learning algorithms\n"
        "- Practice with real-world projects\n"
        "- Prepare for high-paying AI/ML roles"
    )

    return {"result": result}


def build_summarization_agent():
    graph = StateGraph(dict)
    graph.add_node("summarize", summarization_node)
    graph.set_entry_point("summarize")
    return graph.compile()


summarization_agent = build_summarization_agent()
