import os
import base64
import json
from html.parser import HTMLParser

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")


class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._text = []

    def handle_data(self, data):
        self._text.append(data)

    def get_text(self):
        return " ".join(self._text)


def _strip_html(html: str) -> str:
    stripper = _HTMLStripper()
    stripper.feed(html)
    return stripper.get_text()


def _get_service():
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError(
            f"Gmail token not found at '{TOKEN_FILE}'. "
            "Run: python3 daily_assistant.py --auth"
        )
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def _decode_body(payload: dict) -> str:
    """Recursively extract plain text or HTML body from a Gmail message payload."""
    mime = payload.get("mimeType", "")
    body_data = payload.get("body", {}).get("data", "")

    if mime == "text/plain" and body_data:
        return base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")

    if mime == "text/html" and body_data:
        html = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")
        return _strip_html(html)

    for part in payload.get("parts", []):
        result = _decode_body(part)
        if result:
            return result

    return ""


def fetch_expense_emails(max_results: int = 30) -> list:
    """
    Search Gmail for recent receipt/invoice emails (past 2 days).
    Returns a list of dicts: {id, subject, sender, date, snippet, body_text}.
    The agent decides which ones are real expenses.
    """
    service = _get_service()

    query = (
        'subject:(receipt OR invoice OR "order confirmation" OR payment OR "your order")'
        " newer_than:2d"
    )

    result = (
        service.users()
        .messages()
        .list(userId="me", q=query, maxResults=max_results)
        .execute()
    )

    messages = result.get("messages", [])
    emails = []

    for msg_ref in messages:
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=msg_ref["id"], format="full")
            .execute()
        )

        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        body_text = _decode_body(msg.get("payload", {}))

        emails.append(
            {
                "id": msg["id"],
                "subject": headers.get("Subject", "(no subject)"),
                "sender": headers.get("From", ""),
                "date": headers.get("Date", ""),
                "snippet": msg.get("snippet", ""),
                "body_text": body_text[:2000],  # cap to avoid token bloat
            }
        )

    return emails
