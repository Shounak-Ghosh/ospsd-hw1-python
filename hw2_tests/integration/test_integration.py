"""Integration tests for Gmail client functionality."""

from typing import Any

import pytest

from hw2_inbox.implementation.src.implementation.gmail_client import GmailClient

# Constants
NUM_TEST_MESSAGES = 2


@pytest.fixture
def mock_messages_response() -> dict[str, list[dict[str, str]]]:
    """Mock response for messages list."""
    return {
        "messages": [
            {"id": "msg1"},
            {"id": "msg2"},
        ],
    }


@pytest.fixture
def mock_message_content() -> dict[str, Any]:
    """Mock response for message content."""
    return {
        "id": "msg1",
        "payload": {
            "headers": [
                {"name": "Subject", "value": "Test"},
                {"name": "From", "value": "test@example.com"},
            ],
            "body": {"data": "Test content"},
        },
    }


@pytest.fixture
def gmail_client() -> GmailClient:
    """Create a Gmail client."""
    return GmailClient()


def test_mark_as_read_integration(gmail_client: GmailClient) -> None:
    """Test marking email as read."""
    called_with: dict[str, Any] = {}

    class MockMessages:
        def modify(self, **kwargs: dict[str, Any]) -> "MockMessages":
            called_with.update(kwargs)
            return self
        def execute(self) -> dict[str, Any]:
            return {"id": "msg1", "labelIds": ["INBOX"]}

    class MockUsers:
        def messages(self) -> MockMessages:
            return MockMessages()

    class MockService:
        def users(self) -> MockUsers:
            return MockUsers()

    # Mock the service
    gmail_client.service = MockService()  # type: ignore[assignment]

    # Execute
    result = gmail_client.mark_as_read("msg1")

    # Verify
    assert result is True
    assert called_with["id"] == "msg1"
    assert called_with["body"] == {"removeLabelIds": ["UNREAD"]}


def test_get_emails_integration(
    gmail_client: GmailClient,
    mock_messages_response: dict[str, list[dict[str, str]]],
    mock_message_content: dict[str, Any],
) -> None:
    """Test getting emails."""
    class MockMessages:
        def list(self, userId: str, q: str) -> "MockMessages":
            # Simulate the Gmail API's `list` method
            assert userId == "me"  # Ensure the correct userId is passed
            assert q == "test"  # Ensure the query string matches
            self._is_list = True
            return self

        def get(self, userId: str, id: str) -> "MockMessages":
            # Simulate the Gmail API's `get` method
            assert userId == "me"  # Ensure the correct userId is passed
            assert id in ["msg1", "msg2"]  # Ensure the correct message ID is passed
            self._is_get = True
            return self

        def execute(self) -> dict[str, Any]:
            # Return the mocked response
            if hasattr(self, "_is_get"):
                return mock_message_content
            return mock_messages_response

    class MockUsers:
        def messages(self) -> MockMessages:
            return MockMessages()

    class MockService:
        def users(self) -> MockUsers:
            return MockUsers()

    # Mock the service
    gmail_client.service = MockService()  # type: ignore[assignment]

    # Execute
    emails = gmail_client.get_emails("test")

    # Verify
    assert len(emails) == NUM_TEST_MESSAGES
    assert emails[0]["id"] == "msg1"
    assert emails[1]["id"] == "msg2"


def test_detect_spam_integration(gmail_client: GmailClient) -> None:
    """Test spam detection."""
    class MockMessages:
        def get(self, userId: str, id: str) -> "MockMessages":
            # Simulate the Gmail API's `get` method
            assert userId == "me"  # Ensure the correct userId is passed
            assert id == "msg1"  # Ensure the correct message ID is passed
            return self

        def execute(self) -> dict[str, Any]:
            # Return the mocked response
            return {
                "id": "msg1",
                "labelIds": ["INBOX", "SPAM"],
            }

    class MockUsers:
        def messages(self) -> MockMessages:
            return MockMessages()

    class MockService:
        def users(self) -> MockUsers:
            return MockUsers()

    # Mock the service
    gmail_client.service = MockService()  # type: ignore[assignment]

    # Execute
    result = gmail_client.detects_spam_email("msg1")

    # Verify
    assert result is True


def test_unsubscribe_integration(
    gmail_client: GmailClient,
    mock_message_content: dict[str, Any],
) -> None:
    """Test unsubscribe functionality."""
    mock_message_content["payload"]["headers"].append({
        "name": "list-Unsubscribe",
        "value": "<mailto:unsubscribe@example.com>",
    })

    class MockMessages:
        def get(self, userId: str, id: str) -> "MockMessages":
            # Simulate the Gmail API's `get` method
            assert userId == "me"  # Ensure the correct userId is passed
            assert id == "msg1"  # Ensure the correct message ID is passed
            return self

        def execute(self) -> dict[str, Any]:
            # Return the mocked response
            return mock_message_content

    class MockUsers:
        def messages(self) -> MockMessages:
            return MockMessages()

    class MockService:
        def users(self) -> MockUsers:
            return MockUsers()

    # Mock the service
    gmail_client.service = MockService()  # type: ignore[assignment]

    # Execute
    result = gmail_client.unsubscribe_from_email_sender("msg1")

    # Verify
    assert result is True
