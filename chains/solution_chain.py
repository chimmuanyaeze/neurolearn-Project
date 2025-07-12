import os
import json
import re
from pathlib import Path
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
# REMOVED: from langchain_openai import ChatOpenAI
# ADDED: Import the LangChain connector for Google's Generative AI
from langchain_google_genai import ChatGoogleGenerativeAI 

# Load .env file and get API key
# We will now use the GOOGLE_API_KEY environment variable set on Render
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- START OF PATH FIX ---
# Dynamically get the current file's directory
current_dir = Path(__file__).parent

# Construct the path to solution_template relative to current_dir
# solution_chain.py is in 'chains/', and solution_template is in 'prompts/'
# So, from 'chains/', go up one level (..) to the app root, then into 'prompts'
template_path = current_dir.parent / "prompts" / "solution_template"

# Load system prompt template
try:
    with open(template_path, encoding="utf-8") as f:
        template_str = f.read()
except FileNotFoundError:
    # This block will execute if the file is still not found for some reason,
    # providing a fallback or a more explicit error message.
    print(f"Error: Prompt template not found at {template_path}. Using fallback template.")
    # Provide a basic fallback template string or raise a more specific error
    template_str = """
    You are an AI tutor. Given a STEM problem, provide a detailed step-by-step solution,
    including a restatement of the problem, a step-by-step explanation, a visual cue,
    and a final answer. Use the following JSON format:

    {{
      "problem": "Restatement of the problem here.",
      "steps": [
        {{
          "title": "Step 1 Title",
          "explanation": "Detailed explanation for step 1.",
          "visual_cue": "Optional visual cue (e.g., a formula, a graph description, a key term)"
        }},
        {{
          "title": "Step 2 Title",
          "explanation": "Detailed explanation for step 2.",
          "visual_cue": "Optional visual cue"
        }}
      ],
      "final_answer": "The final numerical or conceptual answer."
    }}

    User Problem: {query}
    """
# --- END OF PATH FIX ---


# Set up LangChain prompt
prompt = PromptTemplate(
    input_variables=["query"],
    template=template_str
)

# Initialize LLM (Google Gemini)
# We replace ChatOpenAI with ChatGoogleGenerativeAI and specify a Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro", # Use a suitable Gemini model (e.g., 'gemini-pro' or 'gemini-1.5-pro')
    temperature=0.2,
    # Ensure we pass the GOOGLE_API_KEY retrieved from environment variables
    google_api_key=GOOGLE_API_KEY, 
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
    content = re.sub(r'\\\(|\\\)', '', content)   # Removes \( and \)

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