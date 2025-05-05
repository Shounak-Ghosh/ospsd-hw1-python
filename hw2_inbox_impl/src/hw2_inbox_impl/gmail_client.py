"""Gmail client implementation."""

from __future__ import annotations

import base64
import logging
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

from google.auth.exceptions import GoogleAuthError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore[import]
from googleapiclient.discovery import Resource, build  # type: ignore[import]
from googleapiclient.errors import HttpError  # type: ignore[import]
from hw2_inbox_api import GmailClientInterface

from .constants import GMAIL_SCOPES

logger = logging.getLogger(__name__)

# Error messages
SERVICE_NOT_INITIALIZED = "Gmail service is not initialized"


class GmailClient(GmailClientInterface):
    """Gmail client implementation using Gmail API."""

    def __init__(self) -> None:
        """Initialize Gmail client."""
        self.service: Resource | None = None
        self.user_id = "me"

    def _ensure_service(self) -> Resource:
        """Ensure Gmail service is initialized.
        
        Returns:
            Resource: The initialized Gmail service.
        
        Raises:
            RuntimeError: If the service is not initialized.
        
        """
        if self.service is None:
            raise RuntimeError(SERVICE_NOT_INITIALIZED)
        return self.service

    def connect(self) -> bool:
        """Connect to Gmail service using OAuth2."""
        try:
            creds = None
            token_path = Path("token.json")
            if token_path.exists():
                creds = Credentials.from_authorized_user_file(str(token_path), GMAIL_SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "credentials.json", GMAIL_SCOPES,
                    )
                    creds = flow.run_local_server(port=0)
                token_path.write_text(creds.to_json())

            self.service = build("gmail", "v1", credentials=creds)
        except (GoogleAuthError, HttpError):
            logger.exception("Failed to connect")
            return False
        else:
            return True

    def login(self, _email: str, _password: str) -> bool:
        """Login to Gmail service (not supported by Gmail API)."""
        logger.warning("Gmail API does not support password login. Use OAuth.")
        return False

    def authenticate(self, _email: str, access_token: str) -> bool:
        """Authenticate with Gmail service using access token."""
        try:
            creds = Credentials(token=access_token, scopes=GMAIL_SCOPES)
            self.service = build("gmail", "v1", credentials=creds)
        except (GoogleAuthError, HttpError):
            logger.exception("Failed to authenticate")
            return False
        else:
            return True

    def logout(self) -> None:
        """Logout from Gmail service."""
        token_path = Path("token.json")
        if token_path.exists():
            token_path.unlink()
        self.service = None

    def get_emails(self, query: str) -> list[dict[str, Any]]:
        """Get emails matching the query."""
        try:
            service = self._ensure_service()
            response = (
                service.users()
                .messages()
                .list(userId=self.user_id, q=query)
                .execute()
            )
            messages = response.get("messages", [])
            email_list = []

            for msg in messages[:10]:  # Limit to 10 for performance
                msg_data = (
                    service.users()
                    .messages()
                    .get(userId=self.user_id, id=msg["id"])
                    .execute()
                )
                headers = {
                    h["name"]: h["value"]
                    for h in msg_data["payload"]["headers"]
                }
                snippet = msg_data.get("snippet", "")
                email_list.append({
                    "id": msg["id"],
                    "subject": headers.get("Subject", ""),
                    "sender": headers.get("From", ""),
                    "snippet": snippet,
                })
        except HttpError:
            logger.exception("Failed to get emails")
            return []
        else:
            return email_list

    def get_email_content(self, email_id: str) -> dict[str, Any]:
        """Get content of a specific email."""
        try:
            service = self._ensure_service()
            msg = (
                service.users()
                .messages()
                .get(userId=self.user_id, id=email_id)
                .execute()
            )
            headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
            body = ""
            if "parts" in msg["payload"]:
                for part in msg["payload"]["parts"]:
                    if part["mimeType"] == "text/plain":
                        body = base64.urlsafe_b64decode(
                            part["body"]["data"],
                        ).decode("utf-8")
                        break
            elif "body" in msg["payload"] and "data" in msg["payload"]["body"]:
                body = base64.urlsafe_b64decode(
                    msg["payload"]["body"]["data"],
                ).decode("utf-8")

            return {
                "id": email_id,
                "subject": headers.get("Subject", ""),
                "body": body,
                "headers": headers,
                "attachments": [],
            }
        except (HttpError, ValueError):
            logger.exception("Failed to get email content")
            return {}

    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send an email."""
        try:
            service = self._ensure_service()
            message = MIMEText(body)
            message["to"] = to
            message["subject"] = subject
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
            service.users().messages().send(
                userId=self.user_id,
                body={"raw": raw_message},
            ).execute()
        except (HttpError, ValueError):
            logger.exception("Failed to send email")
            return False
        else:
            return True

    def mark_as_read(self, email_id: str) -> bool:
        """Mark an email as read."""
        try:
            service = self._ensure_service()
            service.users().messages().modify(
                userId=self.user_id,
                id=email_id,
                body={"removeLabelIds": ["UNREAD"]},
            ).execute()
        except HttpError:
            logger.exception("Failed to mark email as read")
            return False
        else:
            return True

    def detects_spam_email(self, email_id: str) -> bool:
        """Detect if an email is spam."""
        try:
            service = self._ensure_service()
            msg = (
                service.users()
                .messages()
                .get(userId=self.user_id, id=email_id)
                .execute()
            )
            return "SPAM" in msg.get("labelIds", [])
        except HttpError:
            logger.exception("Failed to detect spam")
            return False

    def unsubscribe_from_email_sender(self, email_id: str) -> bool:
        """Unsubscribe from an email sender."""
        try:
            service = self._ensure_service()
            msg = (
                service.users()
                .messages()
                .get(userId=self.user_id, id=email_id)
                .execute()
            )
            headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
            return bool(headers.get("list-Unsubscribe", ""))
        except HttpError:
            logger.exception("Failed to unsubscribe")
            return False
