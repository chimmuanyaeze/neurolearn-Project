import os
import json
import re
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY, "Set OPENAI_API_KEY in environment variables"

class Visual(BaseModel):
    type: str = "object"
    content: str
    actions: list = Field(default_factory=list)
    position: str = "CENTER"
    extra: dict = Field(default_factory=dict)

class Step(BaseModel):
    title: str
    explanation: str
    visual: list[Visual] = Field(default_factory=list)

class Solution(BaseModel):
    problem: str
    steps: list[Step]
    final_answer: str

# Load template
current_dir = Path(__file__).parent
template_path = current_dir.parent / "prompts" / "solution_template"
with open(template_path, encoding="utf-8") as f:
    template_str = f.read()

prompt = PromptTemplate(input_variables=["query"], template=template_str)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
solution_chain = prompt | llm

def get_solution(query: str) -> Solution:
    raw = solution_chain.invoke({"query": query})
    content = raw.content.strip()

    # Strip code fences
    content = re.sub(r"```(json)?", "", content).strip()
    content = re.sub(r'\\\(|\\\)', '', content)

    try:
        data = json.loads(content)
        solution = Solution.parse_obj(data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Invalid JSON from LLM:\n{content}") from e

    return solution
