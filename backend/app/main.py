from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import Base, engine, SessionLocal
from app.models.email import Email  # noqa: F401
from app.models.email_analysis import EmailAnalysis  # noqa: F401

from app.services.gmail_service import fetch_new_emails_from_gmail
from app.services.ai_service import analyze_email_with_ollama
from app.services.sync_service import sync_emails_from_gmail

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware
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


@app.get("/emails")
def list_emails():
    """
    Return all saved emails from SQLite.
    """
    db = SessionLocal()
    try:
        emails = db.query(Email).order_by(Email.received_at.desc()).all()
        return [
            {
                "id": e.id,
                "gmail_message_id": e.gmail_message_id,
                "thread_id": e.thread_id,
                "sender": e.sender,
                "subject": e.subject,
                "received_at": e.received_at.isoformat() if e.received_at else None,
            }
            for e in emails
        ]
    finally:
        db.close()


@app.get("/emails/{email_id}")
def get_email(email_id: int):
    """
    Return a single email with full body.
    """
    db = SessionLocal()
    try:
        email = db.query(Email).filter(Email.id == email_id).first()
        if not email:
            return {"detail": "Email not found"}, 404
        return {
            "id": email.id,
            "gmail_message_id": email.gmail_message_id,
            "thread_id": email.thread_id,
            "sender": email.sender,
            "subject": email.subject,
            "body": email.body,
            "received_at": email.received_at.isoformat() if email.received_at else None,
        }
    finally:
        db.close()


@app.post("/sync")
def sync_emails():
    """
    Fetch new emails from Gmail and save to SQLite.
    Returns a summary.
    """
    result = sync_emails_from_gmail(limit=20)
    return result