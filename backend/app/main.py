from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import Base, engine
from app.models.email import Email  # noqa: F401
from app.models.email_analysis import EmailAnalysis  # noqa: F401
from app.services.gmail_service import fetch_one_email
from app.services.ai_service import analyze_email_with_ollama

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware: allow React (Vite) dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "AI Placement Mail Organizer backend is running",
        "status": "ok"
    }


@app.get("/gmail/test")
def gmail_test():
    email_info = fetch_one_email()
    if email_info is None:
        return {"message": "No emails found"}

    return {
        "message": "Fetched one email",
        "email": email_info,
    }


@app.get("/ai/test")
def ai_test():
    sample_email = (
        "Dear Student,\n\n"
        "Amazon is conducting a campus placement drive for the role of SDE Intern. "
        "Eligible branches: CSE, IT, ECE. Eligibility: CGPA >= 7.5. "
        "Deadline to register: 15 August 2026. Please register at "
        "https://placements.amazon.com/register.\n\n"
        "Regards,\n"
        "Training and Placement Cell"
    )

    result = analyze_email_with_ollama(sample_email)
    return {"ai_result": result}


# NEW: Dummy /emails endpoint for React
@app.get("/emails")
def list_emails():
    """
    Return a hard-coded list of emails (dummy data).
    This will later be replaced with real emails from SQLite.
    """
    return [
        {
            "id": 1,
            "company": "Amazon",
            "subject": "SDE Internship",
            "sender": "placements@amazon.com",
            "received_at": "2026-07-26T10:00:00",
        },
        {
            "id": 2,
            "company": "Microsoft",
            "subject": "SDE Intern Hiring Drive",
            "sender": "campus@microsoft.com",
            "received_at": "2026-07-27T09:30:00",
        },
    ]