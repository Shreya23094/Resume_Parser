from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# Set this in your environment or directly here (not recommended in prod)
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "your_huggingface_api_key_here"

# Define your prompt
base_prompt = """
You are a resume parser. Given the raw text of a resume, extract the following:
- Name
- Email
- Phone Number
- Skills (as a list of comma-separated values)

Resume:
{text}

Return the extracted information as a JSON object with keys: "name", "email", "phone", "skills".
"""

llm = HuggingFaceHub(
    repo_id="google/flan-t5-base", model_kwargs={"temperature": 0.5, "max_length": 512}
)

prompt = PromptTemplate(
    input_variables=["text"],
    template=base_prompt
)

llm_chain = LLMChain(prompt=prompt, llm=llm)

def parse_resume(text):
    try:
        result = llm_chain.run(text=text)
        import json
        return json.loads(result)
    except Exception as e:
        return {"name": None, "email": None, "phone": None, "skills": []}

def extract_name(text):
    return parse_resume(text).get("name")

def extract_email(text):
    return parse_resume(text).get("email")

def extract_phone(text):
    return parse_resume(text).get("phone")

def extract_skills(text):
    return parse_resume(text).get("skills", [])
