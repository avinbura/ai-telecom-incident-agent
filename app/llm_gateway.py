import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def get_llm():
    return ChatOpenAI(
        model = "gpt-4o-mini",
        temparature=0
    )

def generate_incident_summary(prompt: str) -> str:
    try:

        llm = get_llm
        response = llm.invoke(prompt)
        return response.content
    except Exception:
        return (
        "Fallback Telecom Incident Summary:\n\n"
        "The telecom monitoring system detected a network issue "
        "requiring operational review. The workflow completed using "
        "rule-based analysis because the LLM service was unavailable."
    )
