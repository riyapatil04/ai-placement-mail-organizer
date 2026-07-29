import requests
from typing import Dict, Any
import json

# Name of the model you pulled with Ollama (adjust if needed)
OLLAMA_MODEL = "gemma3"  # or "gemma3:1b" or "phi3"

# Default Ollama local endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"


def analyze_email_with_ollama(email_text: str) -> Dict[str, Any]:
    """
    Send a placement email to Ollama and ask it to extract structured data.
    Returns a dict with fields like:
    {
      "category": "...",
      "company": "...",
      "role": "...",
      "deadline": "...",
      "eligibility": "...",
      "registration_link": "...",
      "summary": "..."
    }
    """
    prompt = (
        "You are an assistant that analyzes campus placement emails. "
        "Read the following email and extract structured information.\n\n"
        "Return ONLY valid JSON with the following keys:\n"
        "category (\"placement\" or \"other\"),\n"
        "company (string or null),\n"
        "role (string or null),\n"
        "deadline (string or null),\n"
        "eligibility (string or null),\n"
        "registration_link (string or null),\n"
        "summary (string).\n\n"
        "Email:\n"
        f"{email_text}\n\n"
        "Remember: respond ONLY with JSON, no extra text."
    )

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    data = response.json()
    raw_text = data.get("response", "").strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        parsed = {
            "category": "other",
            "company": None,
            "role": None,
            "deadline": None,
            "eligibility": None,
            "registration_link": None,
            "summary": raw_text,
        }

    return parsed