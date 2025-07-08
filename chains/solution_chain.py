import os
import json
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import re

# Load .env file and get API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load system prompt template
with open(r"C:\Users\HP\Documents\projects\neurolearn\prompts\solution_template", encoding="utf-8") as f:
    template_str = f.read()

# Set up LangChain prompt
prompt = PromptTemplate(
    input_variables=["query"],
    template=template_str
)

# Initialize LLM (OpenAI GPT)
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.2,
    openai_api_key=OPENAI_API_KEY,
)

# Chain: prompt → LLM
solution_chain = prompt | llm

# Function to clean and normalize LLM response

def get_solution(query: str) -> dict:
    print(f"🧠 LLM Query: {query}")
    raw = solution_chain.invoke({"query": query})

    content = raw.content.strip()
    print("🧠 Raw Output:", content[:500], "..." if len(content) > 500 else "")

    # Strip common code fences if present
    for tag in ["```json", "```", "json"]:
        if content.startswith(tag):
            content = content[len(tag):].strip()
    if content.endswith("```"):
        content = content[:-3].strip()

    # 🔧 NEW: Remove LaTeX-style math delimiters that break JSON
    content = re.sub(r'\\\(|\\\)', '', content)  # Removes \( and \)

    # Try parsing the JSON
    try:
        result = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"🚨 Invalid JSON from LLM:\n{content}") from e

    # Normalize step formats
    steps = result.get("steps", [])
    normalized_steps = []
    for i, step in enumerate(steps, 1):
        if isinstance(step, dict):
            title = step.get("title", f"Step {i}").strip()
            explanation = step.get("explanation", "").strip()
            visual_cue = step.get("visual_cue", "").strip()
        elif isinstance(step, str):
            if ":" in step:
                title, explanation = step.split(":", 1)
            else:
                title, explanation = f"Step {i}", step
            title, explanation = title.strip(), explanation.strip()
            visual_cue = ""
        else:
            raise ValueError(f"Unexpected step format at index {i}: {step}")

        normalized_steps.append({
            "title": title,
            "explanation": explanation,
            "visual_cue": visual_cue
        })

    result["steps"] = normalized_steps
    return result

