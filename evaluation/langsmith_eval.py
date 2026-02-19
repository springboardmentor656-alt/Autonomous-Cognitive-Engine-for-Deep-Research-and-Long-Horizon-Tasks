from langsmith.evaluation import RunEvaluator, EvaluationResult
from langchain_core.prompts import ChatPromptTemplate
from agent.llm import get_llm

prompt = ChatPromptTemplate.from_template("""
You are evaluating the final output of an autonomous research agent.

Rate the output strictly as one of:
- EXCELLENT
- GOOD
- POOR

Output:
{output}
""")

class QualityEvaluator(RunEvaluator):
    def evaluate_run(self, run, example=None, **kwargs):
        output = run.outputs.get("output", "")

        if not output:
            return EvaluationResult(
                key="quality",
                score=0.0,
                comment="NO_OUTPUT"
            )

        llm = get_llm()
        chain = prompt | llm
        result = chain.invoke({"output": output})

        verdict = result.content.strip().upper()
        score = 1.0 if verdict in ["GOOD", "EXCELLENT"] else 0.0

        return EvaluationResult(
            key="quality",
            score=score,
            comment=verdict
        )
