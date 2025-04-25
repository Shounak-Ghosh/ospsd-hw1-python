"""Integration tests for Gmail client implementation."""

import pytest
from hw2_inbox.implementation.src.implementation.gmail_client import GmailClient

@pytest.fixture
def mock_messages_response():
    """Mock response for messages list."""
    return {
        "messages": [
            {"id": "msg1"},
            {"id": "msg2"}
        ]
    }

@pytest.fixture
def mock_message_content():
    """Mock response for message content."""
    return {
        "id": "msg1",
        "snippet": "Email content",
        "payload": {
            "headers": [
                {"name": "Subject", "value": "Test Subject"},
                {"name": "From", "value": "sender@example.com"}
            ],
            "body": {"data": "VGVzdCBib2R5"}  # Base64 encoded "Test body"
        },
        "labelIds": ["INBOX"]
    }

@pytest.fixture
def gmail_client():
    """Create a Gmail client."""
    return GmailClient()

def test_get_emails_integration(monkeypatch, gmail_client, mock_messages_response):
    """Test getting emails."""
    class MockMessages:
        def list(self, **kwargs):
            return self
        def execute(self):
            return mock_messages_response

    class MockUsers:
        def messages(self):
            return MockMessages()

    class MockService:
        def users(self):
            return MockUsers()

    gmail_client.service = MockService()
    
    # Execute
    emails = gmail_client.get_emails("subject:test")
    
    # Verify
    assert len(emails) == 2
    assert emails[0]["id"] == "msg1"
    assert emails[1]["id"] == "msg2"

def test_get_email_content_integration(monkeypatch, gmail_client, mock_message_content):
    """Test getting email content."""
    class MockMessages:
        def get(self, **kwargs):
            return self
        def execute(self):
            return mock_message_content

    class MockUsers:
        def messages(self):
            return MockMessages()

    class MockService:
        def users(self):
            return MockUsers()

    gmail_client.service = MockService()
    
    # Execute
    content = gmail_client.get_email_content("msg1")
    
    # Verify
    assert content["subject"] == "Test Subject"
    assert content["id"] == "msg1"

def test_mark_as_read_integration(monkeypatch, gmail_client):
    """Test marking email as read."""
    called_with = {}

    class MockMessages:
        def modify(self, **kwargs):
            called_with.update(kwargs)
            return self
        def execute(self):
            return {"id": "msg1", "labelIds": ["INBOX"]}

    class MockUsers:
        def messages(self):
            return MockMessages()

    class MockService:
        def users(self):
            return MockUsers()

    gmail_client.service = MockService()
    
    # Execute
    result = gmail_client.mark_as_read("msg1")
    
    # Verify
    assert result is True
    assert called_with["userId"] == "me"
    assert called_with["id"] == "msg1"
    assert called_with["body"] == {"removeLabelIds": ["UNREAD"]}

def test_send_email_integration(monkeypatch, gmail_client):
    """Test sending email."""
    called_with = {}

    class MockMessages:
        def send(self, **kwargs):
            called_with.update(kwargs)
            return self
        def execute(self):
            return {"id": "msg1"}

    class MockUsers:
        def messages(self):
            return MockMessages()

    class MockService:
        def users(self):
            return MockUsers()

    gmail_client.service = MockService()
    
    # Execute
    result = gmail_client.send_email(
        to="recipient@example.com",
        subject="Test Subject",
        body="Test body"
    )
    
    # Verify
    assert result is True
    assert called_with["userId"] == "me"
    assert "raw" in called_with["body"]

def test_detect_spam_integration(monkeypatch, gmail_client):
    """Test spam detection."""
    class MockMessages:
        def get(self, **kwargs):
            return self
        def execute(self):
            return {
                "id": "msg1",
                "labelIds": ["INBOX", "SPAM"]
            }

    class MockUsers:
        def messages(self):
            return MockMessages()

    class MockService:
        def users(self):
            return MockUsers()

    gmail_client.service = MockService()
    
    # Execute
    result = gmail_client.detects_spam_email("msg1")
    
    # Verify
    assert result is True

def test_unsubscribe_integration(monkeypatch, gmail_client, mock_message_content):
    """Test unsubscribe functionality."""
    mock_message_content["payload"]["headers"].append({
        "name": "List-Unsubscribe",
        "value": "<http://example.com/unsubscribe>"
    })

    class MockMessages:
        def get(self, **kwargs):
            return self
        def execute(self):
            return mock_message_content

    class MockUsers:
        def messages(self):
            return MockMessages()

    class MockService:
        def users(self):
            return MockUsers()

    gmail_client.service = MockService()
    
    # Execute
    result = gmail_client.unsubscribe_from_email_sender("msg1")
    
    # Verify
    assert result is True 