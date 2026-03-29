from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os
import json
from dotenv import load_dotenv

load_dotenv()

class EvaluationResult(BaseModel):
    relevance: float = Field(description="Score for relevance (0.0 - 1.0)")
    completeness: float = Field(description="Score for completeness (0.0 - 1.0)")
    clarity: float = Field(description="Score for clarity (0.0 - 1.0)")
    actionability: float = Field(description="Score for actionability (0.0 - 1.0)")
    overall: float = Field(description="Overall final score (0.0 - 1.0)")

# 🔹 Evaluation prompt for task planning quality
EVALUATION_PROMPT_TEMPLATE = """
You are an expert evaluator of task-planning quality.

Judge how well the generated TODO list satisfies the user's request.

IMPORTANT RULES:
- Do NOT require exact wording
- Do NOT penalize different task order
- Accept multiple valid plans

Evaluate based on:
- Relevance: tasks align with the goal
- Completeness: major steps are present
- Clarity: tasks are understandable
- Actionability: tasks can be executed

Score generously but honestly.

Scoring guide:
0.6–0.7 = acceptable
0.8–0.9 = strong
1.0 = excellent

{format_instructions}

User request:
{input}

Generated TODO list:
{output}

Evaluate the plan using the criteria above.
"""

from agent.config import get_model_name, get_api_key, PRIMARY_PROVIDER

class PlanEvaluator:
    def __init__(self, model_name: str = None):
        model = model_name or get_model_name()
        api_key = get_api_key()
        
        if PRIMARY_PROVIDER == "groq":
            self.llm = ChatGroq(model=model, api_key=api_key)
        elif PRIMARY_PROVIDER == "openai":
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(model=model, api_key=api_key)
        elif PRIMARY_PROVIDER == "anthropic":
            from langchain_anthropic import ChatAnthropic
            self.llm = ChatAnthropic(model=model, api_key=api_key)
        else:
            self.llm = ChatGroq(model=model, api_key=api_key)
            
        self.parser = PydanticOutputParser(pydantic_object=EvaluationResult)
        self.prompt = ChatPromptTemplate.from_template(EVALUATION_PROMPT_TEMPLATE)

    def evaluate(self, user_request: str, generated_plan: list):
        """
        Evaluate a generated plan against the user request.
        """
        if not generated_plan:
            return EvaluationResult(relevance=0, completeness=0, clarity=0, actionability=0, overall=0)

        # Handle both list of steps and raw string
        if isinstance(generated_plan, list):
            formatted_plan = "\n".join([f"{i+1}. {step}" for i, step in enumerate(generated_plan)])
        else:
            formatted_plan = str(generated_plan)
        
        # Prepare the chain
        chain = self.prompt | self.llm | self.parser
        
        try:
            # Invoke the chain
            result = chain.invoke({
                "input": user_request,
                "output": formatted_plan,
                "format_instructions": self.parser.get_format_instructions()
            })
            return result
        except Exception as e:
            print(f"Failed to evaluate or parse: {e}")
            return None

if __name__ == "__main__":
    evaluator = PlanEvaluator()
    
    test_request = "Build a personal website"
    test_plan = ["Choose a framework", "Create a home page", "Deploy to Vercel"]
    
    result = evaluator.evaluate(test_request, test_plan)
    if result:
        print("Evaluation Result:", result.model_dump())
    else:
        print("Evaluation failed.")
