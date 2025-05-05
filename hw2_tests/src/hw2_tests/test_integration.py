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
    """Create and connect a Gmail client."""
    client = gmail_client.GmailClient()
    if not client.connect():
        pytest.skip("Failed to connect to Gmail. Make sure you have valid credentials.")
    return client


@pytest.fixture
def ai_client():
    """Create an AI client."""
    try:
        return api.get_client("cerebras")
    except Exception as e:
        pytest.skip(f"Failed to create AI client: {e}")


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
        def send_message(self, session_id: str, message: str, attachments=None):
            raise RuntimeError("Simulated AI error")
    
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