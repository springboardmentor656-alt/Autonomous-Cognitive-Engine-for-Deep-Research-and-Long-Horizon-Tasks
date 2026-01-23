from langsmith import Client
from langsmith.evaluation import evaluate
from langchain_ollama import OllamaLLM

# LangSmith client
client = Client()

# Load dataset
dataset = client.read_dataset(dataset_name="varshini")

# Ollama model
llm = OllamaLLM(model="llama3")

# -------- MODEL RUN FUNCTION --------
def run(inputs: dict):
    response = llm.invoke(inputs["input"])
    return {"output": response}

# -------- CUSTOM EVALUATOR --------
def correctness_evaluator(run, example):
    """
    Returns:
    - 1.0 if both reference output and model output are null
    - 0.0 otherwise
    """
    reference = example.outputs
    prediction = run.outputs

    if reference is None and prediction is None:
        return {"score": 1.0}

    return {"score": 0.0}

# -------- RUN EVALUATION --------
evaluate(
    run,
    data=dataset,
    evaluators=[correctness_evaluator],
    experiment_prefix="ollama-with-correctness"
)
