# FILE: hw2-inbox/gmail_client.py

from typing import List, Dict, Any
import os
import base64
import json
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GmailClient:
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

    def __init__(self):
        self.service = None
        self.user_id = "me"

    def connect(self) -> bool:
        try:
            creds = None
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                    creds = flow.run_local_server(port=0)
                with open("token.json", "w") as token:
                    token.write(creds.to_json())

            self.service = build("gmail", "v1", credentials=creds)
            return True
        except Exception as e:
            print(f"[connect] Failed: {e}")
            return False

    def login(self, email: str, password: str) -> bool:
        print("[login] Gmail API does not support password login. Use OAuth.")
        return False

    def authenticate(self, email: str, access_token: str) -> bool:
        try:
            creds = Credentials(token=access_token, scopes=self.SCOPES)
            self.service = build("gmail", "v1", credentials=creds)
            return True
        except Exception as e:
            print(f"[authenticate] Failed: {e}")
            return False

    def logout(self) -> None:
        if os.path.exists("token.json"):
            os.remove("token.json")
        self.service = None

    def get_emails(self, query: str) -> List[Dict[str, Any]]:
        try:
            response = self.service.users().messages().list(userId=self.user_id, q=query).execute()
            messages = response.get("messages", [])
            email_list = []

            for msg in messages[:10]:  # Limit to 10 for performance
                msg_data = self.service.users().messages().get(userId=self.user_id, id=msg["id"]).execute()
                headers = {h["name"]: h["value"] for h in msg_data["payload"]["headers"]}
                snippet = msg_data.get("snippet", "")
                email_list.append({
                    "id": msg["id"],
                    "subject": headers.get("Subject", ""),
                    "sender": headers.get("From", ""),
                    "snippet": snippet,
                })

            return email_list
        except Exception as e:
            print(f"[get_emails] Error: {e}")
            return []

    def get_email_content(self, email_id: str) -> Dict[str, Any]:
        try:
            msg = self.service.users().messages().get(userId=self.user_id, id=email_id, format="full").execute()
            headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
            parts = msg["payload"].get("parts", [])
            body = ""

            for part in parts:
                if part["mimeType"] == "text/plain":
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                    break

            return {
                "id": email_id,
                "subject": headers.get("Subject", ""),
                "body": body,
                "headers": headers,
                "attachments": [],
            }
        except Exception as e:
            print(f"[get_email_content] Error: {e}")
            return {}

    def send_email(self, to: str, subject: str, body: str) -> bool:
        try:
            message = MIMEText(body)
            message["to"] = to
            message["subject"] = subject
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            self.service.users().messages().send(userId=self.user_id, body={"raw": raw_message}).execute()
            return True
        except Exception as e:
            print(f"[send_email] Failed: {e}")
            return False

    def mark_as_read(self, email_id: str) -> bool:
        try:
            self.service.users().messages().modify(
                userId=self.user_id,
                id=email_id,
                body={"removeLabelIds": ["UNREAD"]}
            ).execute()
            return True
        except Exception as e:
            print(f"[mark_as_read] Failed: {e}")
            return False

    def detects_spam_email(self, email_id: str) -> bool:
        try:
            msg = self.service.users().messages().get(userId=self.user_id, id=email_id, format="metadata").execute()
            labels = msg.get("labelIds", [])
            return "SPAM" in labels
        except Exception as e:
            print(f"[detects_spam_email] Failed: {e}")
            return False

    def unsubscribe_from_email_sender(self, email_id: str) -> bool:
        try:
            msg = self.service.users().messages().get(userId=self.user_id, id=email_id, format="full").execute()
            headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
            unsubscribe_links = [v for k, v in headers.items() if k.lower() == "list-unsubscribe"]

            if unsubscribe_links:
                print(f"[unsubscribe_from_email_sender] Unsubscribe link: {unsubscribe_links[0]}")
                return True
            return False
        except Exception as e:
            print(f"[unsubscribe_from_email_sender] Failed: {e}")
            return False
