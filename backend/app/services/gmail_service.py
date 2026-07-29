import os
import base64
from typing import List, Dict, Any, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "credentials.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "token.json")


def get_gmail_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


def get_email_body(payload: Dict[str, Any]) -> str:
    """
    Try to extract plain text body from Gmail payload.
    """
    body = ""
    parts = payload.get("parts", [])
    if parts:
        # Try to find text/plain part
        for part in parts:
            mime_type = part.get("mimeType", "")
            if mime_type == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                break
        if not body:
            # Fallback: concatenate all text parts
            texts = []
            for part in parts:
                if part.get("mimeType") == "text/plain":
                    data = part.get("body", {}).get("data", "")
                    if data:
                        texts.append(
                            base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                        )
            body = "\n".join(texts)
    else:
        # Sometimes body is directly in payload.body
        data = payload.get("body", {}).get("data", "")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    return body


def fetch_new_emails_from_gmail(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Fetch up to `limit` recent emails from Gmail and return a list of dicts:
    - gmail_message_id
    - thread_id
    - sender
    - subject
    - date (raw string)
    - body (plain text)
    - snippet
    """
    service = get_gmail_service()

    # List messages (most recent first)
    results = service.users().messages().list(
        userId="me",
        maxResults=limit,
    ).execute()
    messages = results.get("messages", [])

    emails = []

    for msg in messages:
        msg_id = msg["id"]
        raw = service.users().messages().get(
            userId="me",
            id=msg_id,
            format="full",
        ).execute()

        payload = raw.get("payload", {})
        headers = payload.get("headers", [])

        sender = ""
        subject = ""
        date_raw = ""

        for h in headers:
            name = h.get("name")
            value = h.get("value")
            if name == "From":
                sender = value
            elif name == "Subject":
                subject = value
            elif name == "Date":
                date_raw = value

        body = get_email_body(payload)
        snippet = raw.get("snippet", "")

        emails.append(
            {
                "gmail_message_id": msg_id,
                "thread_id": raw.get("threadId", ""),
                "sender": sender,
                "subject": subject,
                "date": date_raw,
                "body": body,
                "snippet": snippet,
            }
        )

    return emails