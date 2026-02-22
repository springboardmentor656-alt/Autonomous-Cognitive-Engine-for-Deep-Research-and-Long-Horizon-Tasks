def finalize_report(state):

    report = "\n\n".join(state["sub_agent_results"])

    state["final_report"] = report
    state["files"]["final_report.md"] = report

    return state
