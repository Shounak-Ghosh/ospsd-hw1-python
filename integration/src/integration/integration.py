"""Integration module for spam detection.

This module integrates a Gmail client and an AI conversation client to detect
spam emails and save the results to a CSV file.
"""
from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from . import constant

if TYPE_CHECKING:
    from ai_conversation_client import api
    from hw2_inbox_impl import gmail_client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpamDetector:
    """A class for detecting spam emails using a Gmail client and an AI client."""

    def __init__(self, mail_client: gmail_client.GmailClient, ai_client: api.AIConversationClient) -> None:
        """Initialize the SpamDetector.

        Args:
            mail_client: An instance of GmailClient for fetching emails.
            ai_client: An instance of AIConversationClient for analyzing emails.

        """
        self.mail_client = mail_client
        self.ai_client = ai_client

    def _get_field(self, email: dict[str, Any], field: str) -> str | None:
        """Safely retrieve a field from an email object.

        Args:
            email: The email object or dictionary.
            field: The field name to retrieve.

        Returns:
            The value of the field, or None if the field does not exist.

        """
        if isinstance(email, dict):
            return email.get(field)
        return getattr(email, field, None)

    def crawl_emails(self, max_count: int, query: str = "") -> list[dict[str, Any]]:
        """Fetch emails from the Gmail client.

        Args:
            max_count: The maximum number of emails to fetch.
            query: The query string to filter emails.

        Returns:
            A list of email objects.

        """
        return self.mail_client.get_emails(query=query)[:max_count]

    def analyze_email(self, session_id: str, email: dict[str, Any]) -> float:
        """Analyze an email and return the spam probability.

        Args:
            session_id: The session ID for the AI client.
            email: The email object to analyze.

        Returns:
            A float representing the spam probability (0.0 to 100.0).

        """
        prompt = f"Analyze the following email:\n\n{email['body']}"
        try:
            response = self.ai_client.send_message(session_id, prompt)
            content = response.get("content", "")
            if isinstance(content, str):
                content = content.strip()
            return float(content) if isinstance(content, str) and content.replace(".", "", 1).isdigit() else 0.0
        except (ValueError, KeyError, AttributeError):
            logger.exception("Error parsing AI response")
            return 0.0
        except Exception:  # Replace with specific exceptions
            logger.exception("Network or API error")
            return 0.0

    def detect_spam(
        self, output_csv: str | None = None, max_emails: int | None = None,
    ) -> None:
        """Run detection and save results to a CSV file.

        Args:
            output_csv: Path to output CSV file. If None, uses DEFAULT_OUTPUT_PATH.
            max_emails: Maximum number of emails to analyze. If None, uses MAX_EMAILS.

        """
        if output_csv is None:
            output_csv = constant.DEFAULT_OUTPUT_PATH
        if max_emails is None:
            max_emails = constant.MAX_EMAILS

        logger.info("Starting spam detection for up to %d emails", max_emails)
        session_id = self.ai_client.start_new_session(user_id="spam_detector")

        try:
            emails = self.crawl_emails(max_count=max_emails)
            logger.info("Fetched %d emails for analysis", len(emails))

            rows = []
            for email in emails:
                pct_spam = self.analyze_email(session_id, email)
                rows.append(
                    {
                        "mail_id": self._get_field(email, "id"),
                        "Pct_spam": pct_spam,
                    },
                )
                logger.info(
                    "Email %s analyzed: %.2f%% spam probability",
                    self._get_field(email, "id"),
                    pct_spam,
                )

            with Path(output_csv).open(mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["mail_id", "Pct_spam"])
                writer.writeheader()
                writer.writerows(rows)
            logger.info("Results saved to %s", output_csv)

        finally:
            self.ai_client.end_session(session_id)
            logger.info("AI session ended")
