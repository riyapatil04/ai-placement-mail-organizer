import os
import requests
from typing import Dict, Any
import json

# Name of the model you pulled with Ollama (adjust if needed)
OLLAMA_MODEL = "gemma3"  # or "gemma3:1b" or "phi3"

# Default Ollama local endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

def _load_prompt(filename: str) -> str:
    base_dir = os.path.dirname(__file__)
    prompts_dir = os.path.join(base_dir, "..", "prompts")
    path = os.path.join(prompts_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def classify_email(email_text: str) -> dict:
    """
    Classify an email into a category using Ollama.
    Returns something like: {"category": "placement"}
    """
    prompt_template = _load_prompt("classify_email.txt")
    prompt = prompt_template.replace("{{EMAIL_TEXT}}", email_text)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    data = response.json()
    raw_text = data.get("response", "").strip()

    import json
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback
        parsed = {"category": "other"}

    # Ensure key exists
    if "category" not in parsed:
        parsed["category"] = "other"

    return parsed

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

def extract_placement(email_text: str) -> dict:
    """
    Extract structured placement information from an email using Ollama.
    Returns a dict with keys:
    company, role, deadline, eligibility, registration_link, summary
    """
    prompt_template = _load_prompt("extract_placement.txt")
    prompt = prompt_template.replace("{{EMAIL_TEXT}}", email_text)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",  # ask Ollama for JSON output [166][168][170][171]
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    data = response.json()
    raw_text = data.get("response", "").strip()

    import json
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback: return all nulls
        parsed = {
            "company": None,
            "role": None,
            "deadline": None,
            "eligibility": None,
            "registration_link": None,
            "summary": "",
        }

    # Ensure all required keys exist
    required_keys = [
        "company",
        "role",
        "deadline",
        "eligibility",
        "registration_link",
        "summary",
    ]
    for k in required_keys:
        if k not in parsed:
            parsed[k] = None

    return parsed

from urllib.parse import urlparse

def validate_placement_extraction(data: dict) -> tuple[bool, list[str]]:
    """
    Basic validation of extracted placement data.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    # company, role, summary can be null, but if present should be non-empty strings
    for field in ["company", "role", "summary"]:
        val = data.get(field)
        if val is not None and not isinstance(val, str):
            errors.append(f"{field} must be string or null")

    # deadline: if present, should be a non-empty string (we won't fully parse dates yet)
    deadline = data.get("deadline")
    if deadline is not None and not isinstance(deadline, str):
        errors.append("deadline must be string or null")

    # eligibility: same
    eligibility = data.get("eligibility")
    if eligibility is not None and not isinstance(eligibility, str):
        errors.append("eligibility must be string or null")

    # registration_link: if present, should be a valid URL
    link = data.get("registration_link")
    if link is not None:
        if not isinstance(link, str):
            errors.append("registration_link must be string or null")
        else:
            parsed = urlparse(link)
            if not parsed.scheme or not parsed.netloc:
                errors.append("registration_link is not a valid URL")

    return len(errors) == 0, errors