import requests
from langsmith import traceable


@traceable(name="web_search_agent")
def web_search_agent(query: str) -> str:
    """Run a lightweight web search and return concise findings."""
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1,
        "skip_disambig": 1,
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as exc:
        return f"Web search failed: {exc}"

    lines = []

    abstract = (data.get("AbstractText") or "").strip()
    if abstract:
        lines.append(f"Summary: {abstract}")

    related = data.get("RelatedTopics") or []
    extracted = []
    for item in related:
        if isinstance(item, dict) and item.get("Text"):
            extracted.append(item["Text"])
        elif isinstance(item, dict) and item.get("Topics"):
            for sub in item.get("Topics", []):
                if isinstance(sub, dict) and sub.get("Text"):
                    extracted.append(sub["Text"])
        if len(extracted) >= 5:
            break

    if extracted:
        lines.append("Top web results:")
        for idx, text in enumerate(extracted[:5], start=1):
            lines.append(f"{idx}. {text}")

    if not lines:
        lines.append("No clear web results were found for this query.")

    return "\n".join(lines)