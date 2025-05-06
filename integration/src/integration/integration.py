"""Integration module for spam detection.

This module integrates a Gmail client and an AI conversation client to detect
spam emails and save the results to a CSV file.
"""
from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ai_conversation_client import api

from . import constant

if TYPE_CHECKING:
    from hw2_inbox_impl import GmailClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpamDetector:
    """Spam detector that uses a mail client and an AI conversation client."""

    def __init__(self, mail_client: GmailClient, ai_client: api.AIConversationClient) -> None:
        """Initialize the SpamDetector.

        Args:
            mail_client: Gmail client instance for fetching emails.
            ai_client: AI conversation client for spam analysis.

        """
        self.mail_client = mail_client
        self.ai_client = ai_client
        logger.info("SpamDetector initialized with mail client and AI client")

    def _get_field(self, email: dict[str, Any] | object, field: str) -> object:
        """Get email field safely.

        Args:
            email: Email object or dictionary.
            field: Field name to get.

        Returns:
            Field value.

        """
        try:
            return email[field]  # Try dictionary access first
        except (KeyError, TypeError):
            return getattr(email, field)  # Fall back to attribute access

    def crawl_emails(self, max_count: int | None = None) -> list[dict[str, object]]:
        """Fetch emails from the mailbox.

        Args:
            max_count: Maximum number of emails to fetch. If None, uses MAX_EMAILS.

        Returns:
            A list of email dictionaries.

        """
        if max_count is None:
            max_count = constant.MAX_EMAILS
        logger.info("Fetching up to %d emails", max_count)
        return list(self.mail_client.get_emails())[:max_count]

    def analyze_email(self, session_id: str, email: dict[str, object]) -> float:
        """Analyze a single email and return spam probability percentage.

        Args:
            session_id: AI conversation session ID.
            email: Email dictionary containing subject, from, to, date, and body.

        Returns:
            Float between 0 and 100 representing spam probability.

        """
        prompt = (
            "You are an email spam classifier. Analyze the following email and determine "
            "the probability that it is spam. Consider these factors:\n"
            "1. Suspicious sender addresses or domains\n"
            "2. Urgent or threatening language\n"
            "3. Requests for personal information or money\n"
            "4. Poor grammar or formatting\n"
            "5. Unusual attachments or links\n\n"
            "Email content:\n"
            f"Subject: {self._get_field(email, 'subject')}\n"
            f"From: {self._get_field(email, 'from_')}\n"
            f"To: {self._get_field(email, 'to')}\n"
            f"Date: {self._get_field(email, 'date')}\n"
            f"Body: {self._get_field(email, 'body')}\n\n"
            "Respond with ONLY a number between 0 and 100 representing the spam probability. "
            "No explanation needed."
        )

        try:
            email_id = self._get_field(email, "id")
            logger.info("Analyzing email %s", email_id)
            response = self.ai_client.send_message(session_id, prompt)
            content = response.get("content", "").strip()
            probability = float(content)
            return max(0.0, min(100.0, probability))  # Clamp to [0, 100]
        except (ValueError, KeyError, AttributeError):
            logger.exception(
                "Error parsing AI response for email %s", self._get_field(email, "id"),
            )
            return 0.0
        except (api.NetworkError, api.APIError):
            logger.exception(
                "Failed to analyze email %s due to network or API error",
                self._get_field(email, "id"),
            )
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
