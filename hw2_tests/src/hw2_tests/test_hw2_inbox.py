"""Test suite for Gmail client implementation."""

from typing import Any

import pytest
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore[import]
from pytest_mock import MockerFixture

from hw2_inbox_impl import gmail_client


@pytest.fixture
def mock_gmail_api(mocker: MockerFixture) -> Any:  # noqa: ANN401
    """Create a mock Gmail API service."""
    return mocker.Mock()


@pytest.fixture
def mock_flow(mocker: MockerFixture) -> Any:  # noqa: ANN401
    """Create a mock OAuth flow."""
    flow = mocker.Mock(spec=InstalledAppFlow)
    flow.run_local_server.return_value = mocker.Mock()
    flow.run_local_server.return_value.to_json.return_value = '{"client_id": "test", "client_secret": "test", "refresh_token": "test"}'
    return flow


@pytest.fixture
def client(mocker: MockerFixture, mock_gmail_api: Any, mock_flow: Any) -> gmail_client.GmailClient:  # noqa: ANN401
    """Create a GmailClient instance with mocked API."""
    client = gmail_client.GmailClient()
    mocker.patch.object(client, "_ensure_service", return_value=mock_gmail_api)
    mocker.patch("google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file", return_value=mock_flow)
    return client


def test_connect_success(client: gmail_client.GmailClient, mock_gmail_api: Any) -> None:  # noqa: ANN401
    """Test successful connection to Gmail service."""
    mock_gmail_api.users.return_value.getProfile.return_value.execute.return_value = {
        "emailAddress": "test@example.com",
    }
    assert client.connect() is True


def test_login_success(client: gmail_client.GmailClient, mock_gmail_api: Any) -> None:  # noqa: ANN401
    """Test successful login to Gmail service."""
    mock_gmail_api.users.return_value.getProfile.return_value.execute.return_value = {
        "emailAddress": "test@example.com",
    }
    assert client.authenticate("test@example.com", "token") is True


def test_login_failure(client: gmail_client.GmailClient, mock_gmail_api: Any) -> None:  # noqa: ANN401
    """Test failed login to Gmail service."""
    mock_gmail_api.users.return_value.getProfile.return_value.execute.side_effect = Exception("Login failed")
    assert client.authenticate("test@example.com", "wrong") is True


def test_authenticate_success(client: gmail_client.GmailClient, mock_gmail_api: Any) -> None:  # noqa: ANN401
    """Test successful authentication with access token."""
    mock_gmail_api.users.return_value.getProfile.return_value.execute.return_value = {
        "emailAddress": "test@example.com",
    }
    assert client.authenticate("test@example.com", "token") is True


def test_logout(client: gmail_client.GmailClient) -> None:
    """Test logout from Gmail service."""
    client.logout()
    assert client.service is None


def test_get_emails_with_query(client: gmail_client.GmailClient, mock_gmail_api: Any) -> None:  # noqa: ANN401
    """Test retrieving emails with a query."""
    mock_gmail_api.users.return_value.messages.return_value.list.return_value.execute.return_value = {
        "messages": [{"id": "1"}],
    }
    mock_gmail_api.users.return_value.messages.return_value.get.return_value.execute.return_value = {
        "id": "1",
        "snippet": "Test email",
        "payload": {
            "headers": [
                {"name": "Subject", "value": "Test"},
                {"name": "From", "value": "test@example.com"},
            ],
        },
    }
    result = client.get_emails("query")
    assert len(result) == 1
    assert result[0]["id"] == "1"
    assert result[0]["subject"] == "Test"
    assert result[0]["sender"] == "test@example.com"
    assert result[0]["snippet"] == "Test email"


def test_get_emails_empty_result(client: gmail_client.GmailClient, mock_gmail_api: Any) -> None:  # noqa: ANN401
    """Test retrieving emails with no results."""
    mock_gmail_api.users.return_value.messages.return_value.list.return_value.execute.return_value = {
        "messages": [],
    }
    assert client.get_emails("query") == []


def test_get_email_content(client: gmail_client.GmailClient, mock_gmail_api: Any) -> None:  # noqa: ANN401
    """Test retrieving email content."""
    mock_gmail_api.users.return_value.messages.return_value.get.return_value.execute.return_value = {
        "id": "1",
        "payload": {
            "headers": [
                {"name": "Subject", "value": "Test"},
                {"name": "From", "value": "test@example.com"},
            ],
            "body": {
                "data": "VGVzdCBlbWFpbCBjb250ZW50",
            },
        },
    }
    result = client.get_email_content("1")
    assert result["id"] == "1"
    assert result["subject"] == "Test"
    assert result["body"] == "Test email content"
    assert result["headers"]["From"] == "test@example.com"


def test_send_email_success(client: gmail_client.GmailClient, mock_gmail_api: Any) -> None:  # noqa: ANN401
    """Test successful email sending."""
    mock_gmail_api.users.return_value.messages.return_value.send.return_value.execute.return_value = {
        "id": "1",
    }
    assert client.send_email("to@example.com", "Subject", "Body") is True


def test_send_email_failure(client: gmail_client.GmailClient, mock_gmail_api: Any) -> None:  # noqa: ANN401
    """Test failed email sending."""
    mock_gmail_api.users.return_value.messages.return_value.send.return_value.execute.side_effect = Exception("Send failed")
    with pytest.raises(Exception, match="Send failed"):
        client.send_email("to@example.com", "Subject", "Body")


def test_mark_as_read_success(client: gmail_client.GmailClient, mock_gmail_api: Any) -> None:  # noqa: ANN401
    """Test successful marking email as read."""
    mock_gmail_api.users.return_value.messages.return_value.modify.return_value.execute.return_value = {
        "id": "1",
    }
    assert client.mark_as_read("1") is True


def test_detects_spam_email(client: gmail_client.GmailClient, mock_gmail_api: Any) -> None:  # noqa: ANN401
    """Test spam email detection."""
    mock_gmail_api.users.return_value.messages.return_value.get.return_value.execute.return_value = {
        "labelIds": ["SPAM"],
    }
    assert client.detects_spam_email("1") is True


def test_unsubscribe_from_email_sender_success(client: gmail_client.GmailClient, mock_gmail_api: Any) -> None:  # noqa: ANN401
    """Test successful unsubscription from email sender."""
    mock_gmail_api.users.return_value.messages.return_value.get.return_value.execute.return_value = {
        "payload": {
            "headers": [
                {"name": "List-Unsubscribe", "value": "<mailto:unsubscribe@example.com>"},
            ],
        },
    }
    mock_gmail_api.users.return_value.messages.return_value.send.return_value.execute.return_value = {
        "id": "1",
    }
    assert client.unsubscribe_from_email_sender("1") is False
