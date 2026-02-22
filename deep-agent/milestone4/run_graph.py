from agent.graph import graph

def main():
    initial_state = {
    "input": "Write a report about blockchain technology.",
    "todos": [],
    "current_task": None,
    "report": "",
    "final_output": ""
}


    result = graph.invoke(initial_state)

    print("\nFinal Output:\n")
    print(result["final_output"])


if __name__ == "__main__":
    main()
