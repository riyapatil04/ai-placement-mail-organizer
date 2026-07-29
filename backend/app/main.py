from fastapi import FastAPI

from app.database.db import Base, engine
from app.models.email import Email  # noqa: F401
from app.models.email_analysis import EmailAnalysis  # noqa: F401
from app.services.gmail_service import fetch_one_email
from app.services.ai_service import analyze_email_with_ollama

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "message": "AI Placement Mail Organizer backend is running",
        "status": "ok"
    }


@app.get("/gmail/test")
def gmail_test():
    """
    Fetch one email from Gmail and return basic info (subject, sender, date).
    """
    email_info = fetch_one_email()
    if email_info is None:
        return {"message": "No emails found"}

    return {
        "message": "Fetched one email",
        "email": email_info,
    }