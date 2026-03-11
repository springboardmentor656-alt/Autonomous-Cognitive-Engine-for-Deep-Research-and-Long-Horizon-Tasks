import os
from typing import TypedDict

from dotenv import load_dotenv
from openai import OpenAI
from langsmith import traceable
from langgraph.graph import StateGraph, END

load_dotenv()

client = OpenAI(
	base_url="https://api.tokenfactory.nebius.com/v1/",
	api_key=os.environ.get("NEBIUS_API_KEY")
)


class SummarizerState(TypedDict):
	text: str
	summary: str


@traceable(name="summarize_node")
def _summarize_node(state: SummarizerState) -> SummarizerState:
	"""Summarize input text."""

	system_prompt = """
You are an expert summarization specialist focused on extracting and synthesizing key information.

Your approach:
- Identify and preserve the most critical information, facts, and decisions
- Maintain logical flow and coherence in the summary
- Highlight key takeaways, action items, or next steps
- Use clear, concise language without losing important nuance
- For longer texts: provide 5-7 sentences capturing main themes
- For shorter texts: provide 2-3 sentences with essential points
- Use bullet points for multiple distinct ideas when appropriate

Focus on what matters most while maintaining accuracy and context."""

	response = client.chat.completions.create(
		model="moonshotai/Kimi-K2-Thinking",
		messages=[
			{"role": "system", "content": system_prompt},
			{"role": "user", "content": state["text"]}
		],
		temperature=0.2,
		max_tokens=350
	)

	raw_choice = response.choices[0] if response and getattr(response, "choices", None) else None
	content = raw_choice.message.content if raw_choice and getattr(raw_choice, "message", None) else None
	summary = content.strip() if content else "Model returned empty content."

	return {"text": state["text"], "summary": summary}


def _build_summarizer_graph():
	builder = StateGraph(SummarizerState)
	builder.add_node("summarize", _summarize_node)
	builder.set_entry_point("summarize")
	builder.add_edge("summarize", END)
	return builder.compile()


summarizer_graph = _build_summarizer_graph()


@traceable(name="summarization_agent")
def summarization_agent(text: str) -> str:
	"""Run summarizer graph and return summary text."""
	result = summarizer_graph.invoke({"text": text, "summary": ""})
	return result.get("summary", "Model returned empty content.")
