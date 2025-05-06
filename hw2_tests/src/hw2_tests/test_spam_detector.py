"""Tests for the SpamDetector class."""

from pathlib import Path
from unittest.mock import Mock

import pytest

from ai_conversation_client import api
from hw2_inbox_impl import gmail_client
from integration import SpamDetector

# Constants
MAX_EMAILS = 2
MAX_SPAM_PROBABILITY = 100


@pytest.fixture
def mock_mail_client() -> Mock:
    """Create a mock GmailClient."""
    client = Mock(spec=gmail_client.GmailClient)
    # Mock email objects with required attributes
    mock_emails = [
        Mock(
            id="email1",
            subject="Test Email 1",
            from_="sender@test.com",
            to="receiver@test.com",
            date="2024-03-20",
            body="This is a test email",
        ),
        Mock(
            id="email2",
            subject="SPAM ALERT",
            from_="spammer@test.com",
            to="receiver@test.com",
            date="2024-03-20",
            body="Buy now! Limited time offer!",
        ),
    ]
    client.get_emails.return_value = mock_emails
    return client


@pytest.fixture
def mock_ai_client() -> Mock:
    """Create a mock AIConversationClient."""
    client = Mock(spec=api.AIConversationClient)
    client.start_new_session.return_value = "test_session"
    client.send_message.return_value = {"content": "75.5"}  # Mock spam probability
    return client


def test_spam_detector_initialization(mock_mail_client: Mock, mock_ai_client: Mock) -> None:
    """Test SpamDetector initialization."""
    detector = SpamDetector(mock_mail_client, mock_ai_client)
    assert detector.mail_client == mock_mail_client
    assert detector.ai_client == mock_ai_client


def test_crawl_emails(mock_mail_client: Mock, mock_ai_client: Mock) -> None:
    """Test email crawling functionality."""
    detector = SpamDetector(mock_mail_client, mock_ai_client)
    emails = detector.crawl_emails(max_count=MAX_EMAILS)
    assert len(emails) == MAX_EMAILS
    mock_mail_client.get_emails.assert_called_once()


def test_analyze_email(mock_mail_client: Mock, mock_ai_client: Mock) -> None:
    """Test email analysis functionality."""
    detector = SpamDetector(mock_mail_client, mock_ai_client)
    email = Mock(
        id="test_email",
        subject="Test Subject",
        from_="test@test.com",
        to="receiver@test.com",
        date="2024-03-20",
        body="Test body",
    )
    
    probability = detector.analyze_email("test_session", email)
    assert 0 <= probability <= MAX_SPAM_PROBABILITY
    mock_ai_client.send_message.assert_called_once()


def test_detect_spam(mock_mail_client: Mock, mock_ai_client: Mock, tmp_path: Path) -> None:
    """Test spam detection and CSV output."""
    detector = SpamDetector(mock_mail_client, mock_ai_client)
    output_file = tmp_path / "spam_results.csv"
    
    detector.detect_spam(str(output_file), max_emails=MAX_EMAILS)
    
    # Verify CSV file was created and contains correct data
    assert output_file.exists()
    with output_file.open() as f:
        content = f.read()
        assert "mail_id" in content
        assert "Pct_spam" in content
        assert "email1" in content
        assert "email2" in content


def test_analyze_email_error_handling(mock_mail_client: Mock, mock_ai_client: Mock) -> None:
    """Test error handling in email analysis."""
    detector = SpamDetector(mock_mail_client, mock_ai_client)
    email = Mock(
        id="test_email",
        subject="Test Subject",
        from_="test@test.com",
        to="receiver@test.com",
        date="2024-03-20",
        body="Test body",
    )
    
    # Test with invalid AI response
    mock_ai_client.send_message.return_value = {"content": "invalid"}
    probability = detector.analyze_email("test_session", email)
    assert probability == 0.0
    
    # Test with network error
    mock_ai_client.send_message.side_effect = Exception("Network error")
    probability = detector.analyze_email("test_session", email)
    assert probability == 0.0
