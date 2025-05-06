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

        def get_emails(self, query: str = "") -> list[dict[str, str]]:
            # Use the `query` argument to filter mock emails
            mock_emails = [
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
            # Filter emails based on the query (case-insensitive match in subject or body)
            return [
                email for email in mock_emails
                if query.lower() in email["subject"].lower() or query.lower() in email["body"].lower()
            ]

    return MockGmailClient()


@pytest.fixture
def ai_client() -> api.AIConversationClient:
    """Create a mock AI client."""
    class MockAIClient(api.AIConversationClient):
        def __init__(self, api_key: str | None = None) -> None:
            self.api_key = api_key or "mock-api-key"

        def start_new_session(self, user_id: str, model: str | None = None) -> str:
            # Log the `user_id` and `model` arguments for debugging
            if model:
                pass
            else:
                pass
            return f"mock-session-id-{user_id}-{model or 'default'}"

        def send_message(self, _: str, __: str, ___: list | None = None) -> dict:
            return {"content": "75.5"}

        def end_session(self, _: str) -> bool:
            return True

        def attach_file(self, _: str, __: str, ___: str | None = None) -> bool:
            return True

        def export_chat_history(self, _: str, __: str = "json") -> str:
            return "{}"

        def switch_model(self, _: str, __: str) -> bool:
            return True

        def get_chat_history(self, _: str, __: int | None = None) -> list:
            return []

        def get_usage_metrics(self, _: str) -> dict:
            return {"token_count": 0}

        def list_available_models(self) -> list[dict[str, str | list[str] | int | bool]]:
            return [{"model_name": "mock-model", "is_default": True}]

        def summarize_conversation(self, _: str) -> str:
            return "Mock summary"

    return MockAIClient()


@pytest.fixture
def spam_detector(mail_client: gmail_client.GmailClient, ai_client: api.AIConversationClient) -> SpamDetector:
    """Create a SpamDetector instance."""
    return SpamDetector(mail_client, ai_client)


def test_spam_detection_handles_ai_errors(spam_detector: SpamDetector, temp_csv_path: Path) -> None:
    """Test that spam detection handles AI client errors gracefully."""
    class ErrorAIClient(api.AIConversationClient):
        def __init__(self, api_key: str | None = None) -> None:
            self.api_key = api_key or "mock-api-key"

        def send_message(self, _: str, __: str, ___: list | None = None) -> NoReturn:
            msg = "Simulated AI error"
            raise RuntimeError(msg)

        def start_new_session(self, user_id: str, model: str | None = None) -> str:
            # Log the `user_id` and `model` arguments for debugging
            if model:
                pass
            else:
                pass
            return f"mock-session-id-{user_id}-{model or 'default'}"

        def end_session(self, _: str) -> bool:
            return True

        def attach_file(self, _: str, __: str, ___: str | None = None) -> bool:
            return True

        def export_chat_history(self, _: str, __: str = "json") -> str:
            return "{}"

        def switch_model(self, _: str, __: str) -> bool:
            return True

        def get_chat_history(self, _: str, __: int | None = None) -> list:
            return []

        def get_usage_metrics(self, _: str) -> dict:
            return {"token_count": 0}

        def list_available_models(self) -> list[dict[str, str | list[str] | int | bool]]:
            return [{"model_name": "mock-model", "is_default": True}]

        def summarize_conversation(self, _: str) -> str:
            return "Mock summary"

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
