"""Integration tests for spam detection functionality."""

from __future__ import annotations

import csv
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, NoReturn

import pytest
from dotenv import load_dotenv

from ai_conversation_client import api
from hw2_inbox_impl import gmail_client
from integration import SpamDetector

if TYPE_CHECKING:
    from collections.abc import Generator

# Constants
MAX_SPAM_PERCENTAGE = 100


@pytest.fixture
def temp_csv_path() -> Generator[Path, None, None]:
    """Create a temporary CSV file path."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        yield Path(f.name)


@pytest.fixture
def mail_client() -> gmail_client.GmailClient:
    """Create a mock Gmail client."""
    class MockGmailClient(gmail_client.GmailClient):
        def connect(self) -> bool:
            return True

        def get_emails(self, _: str = "") -> list[dict[str, str]]:
            # Return some mock emails
            return [
                {
                    "id": "1",
                    "subject": "Test Email 1",
                    "from_": "sender1@example.com",
                    "to": "recipient@example.com",
                    "date": "2024-03-20",
                    "body": "This is a test email 1",
                },
                {
                    "id": "2",
                    "subject": "Test Email 2",
                    "from_": "sender2@example.com",
                    "to": "recipient@example.com",
                    "date": "2024-03-20",
                    "body": "This is a test email 2",
                },
            ]

    return MockGmailClient()


@pytest.fixture
def ai_client() -> api.AIConversationClient:
    """Create a mock AI client."""
    class MockAIClient(api.AIConversationClient):
        def __init__(self, api_key: str | None = None) -> None:
            self.api_key = api_key or "mock-api-key"

        def start_new_session(self, _: str, __: str | None = None) -> str:
            return "mock-session-id"

        def send_message(self, _: str, __: str, ___: list | None = None) -> dict:
            return {"content": "75.5"}  # 75.5% spam probability

        def end_session(self, _: str) -> bool:
            return True

    return MockAIClient()


@pytest.fixture
def spam_detector(mail_client: gmail_client.GmailClient, ai_client: api.AIConversationClient) -> SpamDetector:
    """Create a SpamDetector instance."""
    return SpamDetector(mail_client, ai_client)


def test_spam_detection_creates_csv(spam_detector: SpamDetector, temp_csv_path: Path) -> None:
    """Test that spam detection creates a CSV file with expected format."""
    spam_detector.detect_spam(output_csv=str(temp_csv_path), max_emails=5)

    # Verify CSV file exists
    assert temp_csv_path.exists(), "CSV file was not created"

    # Verify CSV content
    with temp_csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        # Check header
        assert reader.fieldnames == ["mail_id", "Pct_spam"], "CSV has incorrect headers"

        # Check we have some rows
        assert len(rows) > 0, "CSV has no data rows"

        # Check each row has required fields and valid values
        for row in rows:
            assert "mail_id" in row, "Row missing mail_id"
            assert "Pct_spam" in row, "Row missing Pct_spam"

            # Verify spam percentage is a valid number between 0 and 100
            spam_pct = float(row["Pct_spam"])
            assert 0 <= spam_pct <= MAX_SPAM_PERCENTAGE, f"Invalid spam percentage: {spam_pct}"


def test_spam_detection_respects_max_emails(spam_detector: SpamDetector, temp_csv_path: Path) -> None:
    """Test that spam detection respects the max_emails parameter."""
    max_emails = 3
    spam_detector.detect_spam(output_csv=str(temp_csv_path), max_emails=max_emails)

    with temp_csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) <= max_emails, f"Got {len(rows)} rows, expected at most {max_emails}"


def test_spam_detection_handles_empty_inbox(spam_detector: SpamDetector, temp_csv_path: Path) -> None:
    """Test that spam detection handles an empty inbox gracefully."""
    class EmptyMailClient(gmail_client.GmailClient):
        def connect(self) -> bool:
            return True

        def get_emails(self, _: str = "") -> list:
            return []

    empty_detector = SpamDetector(EmptyMailClient(), spam_detector.ai_client)
    empty_detector.detect_spam(output_csv=str(temp_csv_path))

    # Verify CSV file exists but is empty (only has header)
    assert temp_csv_path.exists(), "CSV file was not created"
    with temp_csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 0, "CSV should be empty for empty inbox"


def test_spam_detection_handles_ai_errors(spam_detector: SpamDetector, temp_csv_path: Path) -> None:
    """Test that spam detection handles AI client errors gracefully."""
    class ErrorAIClient(api.AIConversationClient):
        def send_message(self, _: str, __: str, ___: list | None = None) -> NoReturn:
            msg = "Simulated AI error"
            raise RuntimeError(msg)

    error_detector = SpamDetector(spam_detector.mail_client, ErrorAIClient())
    error_detector.detect_spam(output_csv=str(temp_csv_path), max_emails=1)

    # Verify CSV file exists and has a row with 0% spam (error case)
    assert temp_csv_path.exists(), "CSV file was not created"
    with temp_csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) > 0, "CSV should have at least one row"
        assert float(rows[0]["Pct_spam"]) == 0.0, "Error case should result in 0% spam"


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Run tests
    pytest.main([__file__, "-v"])
