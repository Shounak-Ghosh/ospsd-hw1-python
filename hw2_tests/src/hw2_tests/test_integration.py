"""Integration tests for spam detection functionality."""

import csv
import os
import tempfile
from pathlib import Path
import pytest
from dotenv import load_dotenv

from hw2_inbox_impl import gmail_client
from ai_conversation_client import api
from integration import SpamDetector


@pytest.fixture
def temp_csv_path():
    """Create a temporary CSV file path."""
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        return f.name


@pytest.fixture
def mail_client():
    """Create a mock Gmail client."""
    class MockGmailClient(gmail_client.GmailClient):
        def connect(self) -> bool:
            return True
            
        def get_emails(self, query: str = "") -> list:
            # Return some mock emails
            return [
                {
                    "id": "1",
                    "subject": "Test Email 1",
                    "from_": "sender1@example.com",
                    "to": "recipient@example.com",
                    "date": "2024-03-20",
                    "body": "This is a test email 1"
                },
                {
                    "id": "2",
                    "subject": "Test Email 2",
                    "from_": "sender2@example.com",
                    "to": "recipient@example.com",
                    "date": "2024-03-20",
                    "body": "This is a test email 2"
                }
            ]
    
    return MockGmailClient()


@pytest.fixture
def ai_client():
    """Create a mock AI client."""
    class MockAIClient(api.AIConversationClient):
        def __init__(self, api_key: str | None = None) -> None:
            """Initialize mock AI client."""
            self.api_key = api_key or "mock-api-key"
            
        def start_new_session(self, user_id: str, model: str | None = None) -> str:
            return "mock-session-id"
            
        def send_message(self, session_id: str, message: str, attachments=None):
            # Return a mock response with a spam probability
            return {"content": "75.5"}  # 75.5% spam probability
            
        def end_session(self, session_id: str) -> bool:
            return True
            
        def get_chat_history(self, session_id: str, limit: int | None = None) -> list:
            return []
            
        def list_available_models(self) -> list:
            return [
                {
                    "id": "mock-model",
                    "name": "Mock Model",
                    "capabilities": ["text-generation", "chat"],
                    "max_tokens": 8192
                }
            ]
            
        def switch_model(self, session_id: str, model_id: str) -> bool:
            return True
            
        def attach_file(self, session_id: str, file_path: str, description: str | None = None) -> bool:
            return True
            
        def export_chat_history(self, session_id: str, format: str = "json") -> str:
            return "{}"
            
        def get_usage_metrics(self, session_id: str) -> dict:
            return {
                "token_count": 0,
                "api_calls": 0,
                "cost_estimate": 0.0
            }
            
        def summarize_conversation(self, session_id: str) -> str:
            return "Mock conversation summary"
    
    return MockAIClient()


@pytest.fixture
def spam_detector(mail_client, ai_client):
    """Create a SpamDetector instance."""
    return SpamDetector(mail_client, ai_client)


def test_spam_detection_creates_csv(spam_detector, temp_csv_path):
    """Test that spam detection creates a CSV file with expected format."""
    # Run spam detection
    spam_detector.detect_spam(output_csv=temp_csv_path, max_emails=5)
    
    # Verify CSV file exists
    assert os.path.exists(temp_csv_path), "CSV file was not created"
    
    # Verify CSV content
    with open(temp_csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        # Check header
        assert reader.fieldnames == ['mail_id', 'Pct_spam'], "CSV has incorrect headers"
        
        # Check we have some rows
        assert len(rows) > 0, "CSV has no data rows"
        
        # Check each row has required fields and valid values
        for row in rows:
            assert 'mail_id' in row, "Row missing mail_id"
            assert 'Pct_spam' in row, "Row missing Pct_spam"
            
            # Verify spam percentage is a valid number between 0 and 100
            try:
                spam_pct = float(row['Pct_spam'])
                assert 0 <= spam_pct <= 100, f"Invalid spam percentage: {spam_pct}"
            except ValueError:
                pytest.fail(f"Invalid spam percentage value: {row['Pct_spam']}")


def test_spam_detection_respects_max_emails(spam_detector, temp_csv_path):
    """Test that spam detection respects the max_emails parameter."""
    max_emails = 3
    spam_detector.detect_spam(output_csv=temp_csv_path, max_emails=max_emails)
    
    with open(temp_csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) <= max_emails, f"Got {len(rows)} rows, expected at most {max_emails}"


def test_spam_detection_handles_empty_inbox(spam_detector, temp_csv_path):
    """Test that spam detection handles an empty inbox gracefully."""
    # Create a mock mail client that returns no emails
    class EmptyMailClient(gmail_client.GmailClient):
        def connect(self) -> bool:
            return True
            
        def get_emails(self, query: str = "") -> list:
            return []
    
    empty_detector = SpamDetector(EmptyMailClient(), spam_detector.ai_client)
    empty_detector.detect_spam(output_csv=temp_csv_path)
    
    # Verify CSV file exists but is empty (only has header)
    assert os.path.exists(temp_csv_path), "CSV file was not created"
    with open(temp_csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 0, "CSV should be empty for empty inbox"


def test_spam_detection_handles_ai_errors(spam_detector, temp_csv_path):
    """Test that spam detection handles AI client errors gracefully."""
    # Create a mock AI client that raises an error
    class ErrorAIClient(api.AIConversationClient):
        def __init__(self, api_key: str | None = None) -> None:
            self.api_key = api_key or "mock-api-key"
            
        def start_new_session(self, user_id: str, model: str | None = None) -> str:
            return "mock-session-id"
            
        def send_message(self, session_id: str, message: str, attachments=None):
            raise RuntimeError("Simulated AI error")
            
        def end_session(self, session_id: str) -> bool:
            return True
            
        def get_chat_history(self, session_id: str, limit: int | None = None) -> list:
            return []
            
        def list_available_models(self) -> list:
            return [
                {
                    "id": "mock-model",
                    "name": "Mock Model",
                    "capabilities": ["text-generation", "chat"],
                    "max_tokens": 8192
                }
            ]
            
        def switch_model(self, session_id: str, model_id: str) -> bool:
            return True
            
        def attach_file(self, session_id: str, file_path: str, description: str | None = None) -> bool:
            return True
            
        def export_chat_history(self, session_id: str, format: str = "json") -> str:
            return "{}"
            
        def get_usage_metrics(self, session_id: str) -> dict:
            return {
                "token_count": 0,
                "api_calls": 0,
                "cost_estimate": 0.0
            }
            
        def summarize_conversation(self, session_id: str) -> str:
            return "Mock conversation summary"
    
    error_detector = SpamDetector(spam_detector.mail_client, ErrorAIClient())
    error_detector.detect_spam(output_csv=temp_csv_path, max_emails=1)
    
    # Verify CSV file exists and has a row with 0% spam (error case)
    assert os.path.exists(temp_csv_path), "CSV file was not created"
    with open(temp_csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) > 0, "CSV should have at least one row"
        assert float(rows[0]['Pct_spam']) == 0.0, "Error case should result in 0% spam"


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Run tests
    pytest.main([__file__, "-v"]) 