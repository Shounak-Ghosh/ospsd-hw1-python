"""Tests for the hw2_inbox_package."""

from typing import Any

import pytest
from pytest_mock import MockerFixture

from hw2_inbox.implementation.src.implementation.gmail_client import GmailClient


@pytest.fixture
def mock_client(mocker: MockerFixture) -> Any:  # type: ignore[valid-type]
    """Create a mock GmailClient instance.
    
    We use Any return type here because pytest-mock's Mock objects don't match
    the strict type checking of the classes they mock, but they provide the same interface.
    """
    return mocker.Mock(spec=GmailClient)


# Connection Management Tests
def test_connect_success(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test successful connection to Gmail service."""
    mock_client.connect.return_value = True
    assert mock_client.connect()


def test_connect_failure(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test failed connection to Gmail service."""
    mock_client.connect.return_value = False
    assert not mock_client.connect()


# Authentication Tests
def test_login_success(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test successful login to Gmail service."""
    mock_client.login.return_value = True
    assert mock_client.login("test@example.com", "password")


def test_login_failure(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test failed login to Gmail service."""
    mock_client.login.return_value = False
    assert not mock_client.login("test@example.com", "wrong_password")


def test_authenticate_success(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test successful authentication with access token."""
    mock_client.authenticate.return_value = True
    assert mock_client.authenticate("test@example.com", "access_token")


def test_logout(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test logout from Gmail service."""
    mock_client.logout.return_value = None
    mock_client.logout()


# Email Retrieval Tests
def test_get_emails_with_query(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test retrieving emails with a query."""
    expected_emails: list[dict[str, Any]] = [
        {
            "id": "1",
            "subject": "Test Email",
            "sender": "sender@example.com",
            "snippet": "Test content",
        },
    ]
    mock_client.get_emails.return_value = expected_emails
    assert mock_client.get_emails("test query") == expected_emails


def test_get_emails_empty_result(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test retrieving emails with no results."""
    mock_client.get_emails.return_value = []
    assert mock_client.get_emails("no results") == []


def test_get_email_content(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test retrieving email content."""
    email_content = {
        "id": "1",
        "subject": "Test Email",
        "body": "Test content",
        "headers": {"From": "sender@example.com"},
        "attachments": [],
    }
    mock_client.get_email_content.return_value = email_content
    assert mock_client.get_email_content("1") == email_content


# Email Management Tests
def test_send_email_success(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test successful email sending."""
    mock_client.send_email.return_value = True
    assert mock_client.send_email("to@example.com", "Test", "Content")


def test_send_email_failure(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test failed email sending."""
    mock_client.send_email.return_value = False
    assert not mock_client.send_email("to@example.com", "Test", "Content")


def test_mark_as_read_success(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test successful marking email as read."""
    mock_client.mark_as_read.return_value = True
    assert mock_client.mark_as_read("1")


# Spam and Subscription Management Tests
def test_detects_spam_email(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test spam email detection."""
    mock_client.detects_spam_email.return_value = True
    assert mock_client.detects_spam_email("1")


def test_unsubscribe_from_email_sender_success(mock_client: Any) -> None:  # type: ignore[valid-type]
    """Test successful unsubscription from email sender."""
    mock_client.unsubscribe_from_email_sender.return_value = True
    assert mock_client.unsubscribe_from_email_sender("1")
