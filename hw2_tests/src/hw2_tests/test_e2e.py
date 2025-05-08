"""End-to-end tests for the spam detection system."""

from __future__ import annotations

import csv
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from dotenv import load_dotenv

from ai_conversation_client import api
from hw2_inbox_impl import gmail_client
from integration import SpamDetector

if TYPE_CHECKING:
    from collections.abc import Generator

# Constants
MAX_EMAILS = 5
MAX_SPAM_PERCENTAGE = 100


@pytest.fixture
def temp_csv_path() -> Generator[Path, None, None]:
    """Create a temporary CSV file path."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        yield Path(f.name)


@pytest.fixture
def mail_client() -> gmail_client.GmailClient:
    """Create a mock Gmail client with realistic test data."""
    class MockGmailClient(gmail_client.GmailClient):
        def connect(self) -> bool:
            return True

        def get_emails(self, query: str = "") -> list[dict[str, str]]:
            mock_emails = [
                {
                    "id": "1",
                    "subject": "Important Meeting Tomorrow",
                    "from_": "colleague@company.com",
                    "to": "user@company.com",
                    "date": "2024-03-20",
                    "body": "Please join the team meeting at 10 AM tomorrow.",
                },
                {
                    "id": "2",
                    "subject": "URGENT: Your Account Needs Verification",
                    "from_": "security@bank.com",
                    "to": "user@company.com",
                    "date": "2024-03-20",
                    "body": "Click here to verify your account immediately!",
                },
                {
                    "id": "3",
                    "subject": "Project Update",
                    "from_": "manager@company.com",
                    "to": "user@company.com",
                    "date": "2024-03-20",
                    "body": "The project is on track and meeting all milestones.",
                },
                {
                    "id": "4",
                    "subject": "WIN A FREE IPHONE!",
                    "from_": "giveaway@spam.com",
                    "to": "user@company.com",
                    "date": "2024-03-20",
                    "body": "Congratulations! You've been selected to win a free iPhone!",
                },
                {
                    "id": "5",
                    "subject": "Team Lunch Next Week",
                    "from_": "hr@company.com",
                    "to": "user@company.com",
                    "date": "2024-03-20",
                    "body": "Join us for a team lunch next Thursday at noon.",
                },
            ]
            return [
                email for email in mock_emails
                if query.lower() in email["subject"].lower() or query.lower() in email["body"].lower()
            ]

    return MockGmailClient()


@pytest.fixture
def ai_client() -> api.AIConversationClient:
    """Create a mock AI client that returns realistic spam probabilities."""
    class MockAIClient(api.AIConversationClient):
        def __init__(self, api_key: str | None = None) -> None:
            self.api_key = api_key or "mock-api-key"

        def start_new_session(self, user_id: str, model: str | None = None) -> str:
            return f"mock-session-id-{user_id}-{model or 'default'}"

        def send_message(self, _: str, message: str, __: list | None = None) -> dict:
            # Return different spam probabilities based on email content
            if "URGENT" in message or "WIN" in message or "FREE" in message:
                return {"content": "85.5"}
            if "meeting" in message.lower() or "project" in message.lower():
                return {"content": "5.5"}
            return {"content": "25.5"}

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


def test_complete_spam_detection_flow(spam_detector: SpamDetector, temp_csv_path: Path) -> None:
    """Test the complete spam detection flow from email retrieval to CSV output."""
    # Run spam detection
    spam_detector.detect_spam(output_csv=str(temp_csv_path), max_emails=MAX_EMAILS)

    # Verify CSV file exists and has the correct structure
    assert temp_csv_path.exists(), "CSV file was not created"
    
    with temp_csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        # Verify we got all emails
        assert len(rows) == MAX_EMAILS, f"Expected {MAX_EMAILS} emails, got {len(rows)}"
        
        # Verify CSV structure
        required_fields = {"mail_id", "Pct_spam"}
        assert all(field in rows[0] for field in required_fields), "Missing required fields in CSV"
        
        # Verify spam probabilities are within valid range
        for row in rows:
            spam_pct = float(row["Pct_spam"])
            assert 0 <= spam_pct <= MAX_SPAM_PERCENTAGE, f"Invalid spam percentage: {spam_pct}"


def test_spam_detection_with_query_filter(spam_detector: SpamDetector, temp_csv_path: Path) -> None:
    """Test spam detection with a specific query filter."""
    # Run spam detection
    spam_detector.detect_spam(output_csv=str(temp_csv_path), max_emails=MAX_EMAILS)
    
    # Verify CSV file exists and contains filtered results
    assert temp_csv_path.exists(), "CSV file was not created"
    
    with temp_csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        # Verify we got the correct number of emails
        assert len(rows) > 0, "No emails found"
        
        # Verify spam probabilities are within valid range
        for row in rows:
            spam_pct = float(row["Pct_spam"])
            assert 0 <= spam_pct <= MAX_SPAM_PERCENTAGE, f"Invalid spam percentage: {spam_pct}"


def test_spam_detection_with_max_emails_limit(spam_detector: SpamDetector, temp_csv_path: Path) -> None:
    """Test spam detection with a maximum email limit."""
    max_emails = 2
    
    # Run spam detection with a limit
    spam_detector.detect_spam(output_csv=str(temp_csv_path), max_emails=max_emails)
    
    # Verify CSV file exists and contains limited results
    assert temp_csv_path.exists(), "CSV file was not created"
    
    with temp_csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        # Verify we got the correct number of emails
        assert len(rows) == max_emails, f"Expected {max_emails} emails, got {len(rows)}"


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Run tests
    pytest.main([__file__, "-v"])
