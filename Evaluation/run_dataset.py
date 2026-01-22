from dotenv import load_dotenv
load_dotenv()

from langsmith import Client
from langsmith.evaluation import evaluate

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from Evaluation.planning_evaluator import PlanningAccuracyEvaluator


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

prompt = PromptTemplate.from_template(
    """
You are a planning agent.

Task:
{task}

Break this task into a clear, ordered list of TODO steps.
Return each step on a new line.
"""
)

chain = prompt | llm | StrOutputParser()


# ✅ TARGET FUNCTION (must accept inputs)
def run_chain(inputs: dict):
    return chain.invoke(inputs)


client = Client()

dataset = client.read_dataset(
    dataset_name="milestone1-task-planning"
)

evaluate(
    run_chain,                      # ✅ NOT chain_factory
    data=dataset.name,
    evaluators=[PlanningAccuracyEvaluator()],
)
