from datetime import datetime
from typing import List, Dict, Any

from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.models.email import Email
from app.services.gmail_service import fetch_new_emails_from_gmail


def sync_emails_from_gmail(limit: int = 20) -> Dict[str, Any]:
    """
    Fetch new emails from Gmail and save them to SQLite.
    Returns a summary: how many fetched, how many new, how many duplicates.
    """
    db: Session = SessionLocal()
    try:
        gmail_emails = fetch_new_emails_from_gmail(limit=limit)

        fetched_count = len(gmail_emails)
        new_count = 0
        duplicate_count = 0

        for g_email in gmail_emails:
            # Check duplicate
            existing = (
                db.query(Email)
                .filter(Email.gmail_message_id == g_email["gmail_message_id"])
                .first()
            )
            if existing:
                duplicate_count += 1
                continue

            # Parse received_at (simple approach: use current time)
            # For a more accurate approach, parse g_email["date"] with dateparser later.
            received_at = datetime.utcnow()

            new_email = Email(
                gmail_message_id=g_email["gmail_message_id"],
                thread_id=g_email["thread_id"],
                sender=g_email["sender"],
                subject=g_email["subject"],
                body=g_email["body"],
                received_at=received_at,
                is_processed=False,
            )
            db.add(new_email)
            new_count += 1

        db.commit()

        return {
            "fetched": fetched_count,
            "new": new_count,
            "duplicates": duplicate_count,
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()