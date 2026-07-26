import os
from typing import Optional, Dict, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Readonly Gmail scope for now
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Paths relative to backend/app execution context
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "credentials.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "token.json")


def get_gmail_service():
    """
    Authenticate with Gmail using OAuth and return a Gmail API service object.
    On first run, opens a browser, asks you to log in and grant access, then saves token.json.
    On later runs, reuses token.json so you don't have to log in again.
    """
    creds = None

    # Load saved token if it exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials, do the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    # Build the Gmail API service
    service = build("gmail", "v1", credentials=creds)
    return service


def fetch_one_email() -> Optional[Dict[str, Any]]:
    """
    Fetch the most recent email from your Gmail inbox and return basic info:
    sender, subject, date.
    """
    service = get_gmail_service()

    # List messages, just 1
    results = service.users().messages().list(userId="me", maxResults=1).execute()
    messages = results.get("messages", [])

    if not messages:
        return None

    msg_id = messages[0]["id"]
    msg = service.users().messages().get(userId="me", id=msg_id, format="full").execute()

    headers = msg.get("payload", {}).get("headers", [])
    info = {"id": msg_id}

    for h in headers:
        name = h.get("name")
        value = h.get("value")
        if name == "Subject":
            info["subject"] = value
        elif name == "From":
            info["sender"] = value
        elif name == "Date":
            info["date"] = value

    return info