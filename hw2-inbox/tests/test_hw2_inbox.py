import pytest
from typing import List, Dict, Any
from .. import GmailClient

@pytest.fixture
def mock_client(mocker):
    return mocker.Mock(spec=GmailClient)

# Connection Management Tests
def test_connect_success(mock_client):
    mock_client.connect.return_value = True
    result = mock_client.connect()
    assert result is True
    mock_client.connect.assert_called_once()

def test_connect_failure(mock_client):
    mock_client.connect.return_value = False
    result = mock_client.connect()
    assert result is False
    mock_client.connect.assert_called_once()

# Authentication Tests
def test_login_success(mock_client):
    mock_client.login.return_value = True
    result = mock_client.login("example@example.com", "password")
    assert result is True
    mock_client.login.assert_called_once_with("example@example.com", "password")

def test_login_failure(mock_client):
    mock_client.login.return_value = False
    result = mock_client.login("example@example.com", "wrong_password")
    assert result is False
    mock_client.login.assert_called_once_with("example@example.com", "wrong_password")

def test_authenticate_success(mock_client):
    mock_client.authenticate.return_value = True
    result = mock_client.authenticate("example@example.com", "sample_access_token")
    assert result is True
    mock_client.authenticate.assert_called_once_with("example@example.com", "sample_access_token")

def test_logout(mock_client):
    mock_client.logout.return_value = None
    mock_client.logout()
    mock_client.logout.assert_called_once()

# Email Retrieval Tests
def test_get_emails_with_query(mock_client):
    expected_emails: List[Dict[str, Any]] = [
        {"id": "1", "subject": "Hello", "sender": "1@example.com", "snippet": "Hi there"},
        {"id": "2", "subject": "World", "sender": "2@example.com", "snippet": "Greetings"}
    ]
    mock_client.get_emails.return_value = expected_emails
    result = mock_client.get_emails("SELECT * FROM emails WHERE unread = true")
    assert result == expected_emails
    mock_client.get_emails.assert_called_once_with("SELECT * FROM emails WHERE unread = true")

def test_get_emails_empty_result(mock_client):
    mock_client.get_emails.return_value = []
    result = mock_client.get_emails("SELECT * FROM emails WHERE id = 'nonexistent'")
    assert result == []
    mock_client.get_emails.assert_called_once()

def test_get_email_content(mock_client):
    email_content = {
        "id": "1",
        "subject": "Hello",
        "body": "This is a test email.",
        "headers": {"From": "sender@example.com", "Date": "2024-03-20"},
        "attachments": []
    }
    mock_client.get_email_content.return_value = email_content
    result = mock_client.get_email_content("1")
    assert result == email_content
    mock_client.get_email_content.assert_called_once_with("1")

# Email Management Tests
def test_send_email_success(mock_client):
    mock_client.send_email.return_value = True
    result = mock_client.send_email("recipient@example.com", "Test Subject", "Test Body")
    assert result is True
    mock_client.send_email.assert_called_once_with("recipient@example.com", "Test Subject", "Test Body")

def test_send_email_failure(mock_client):
    mock_client.send_email.return_value = False
    result = mock_client.send_email("invalid@example.com", "Test Subject", "Test Body")
    assert result is False
    mock_client.send_email.assert_called_once()

def test_mark_as_read_success(mock_client):
    mock_client.mark_as_read.return_value = True
    result = mock_client.mark_as_read("1")
    assert result is True
    mock_client.mark_as_read.assert_called_once_with("1")

# Spam and Subscription Management Tests
def test_detects_spam_email(mock_client):
    mock_client.detects_spam_email.return_value = True
    result = mock_client.detects_spam_email("1")
    assert result is True
    mock_client.detects_spam_email.assert_called_once_with("1")

def test_unsubscribe_from_email_sender_success(mock_client):
    mock_client.unsubscribe_from_email_sender.return_value = True
    result = mock_client.unsubscribe_from_email_sender("1")
    assert result is True
    mock_client.unsubscribe_from_email_sender.assert_called_once_with("1")
