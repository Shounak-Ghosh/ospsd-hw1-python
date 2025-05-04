"""Test module for Gmail client interface.

This module contains tests for the GmailClientInterface abstract base class
and its implementations.
"""

import pytest

from hw2_inbox_api import GmailClientInterface


class MockGmailClient(GmailClientInterface):
    """Mock implementation of GmailClientInterface for testing."""
    
    def connect(self) -> bool:
        """Establish a connection to the Gmail service.
        
        Returns:
            bool: Always returns True for testing purposes.

        """
        return True
        
    def login(self, username: str, password: str) -> bool:
        """Authenticate with username and password.
        
        Args:
            username: The email address to login with.
            password: The password for authentication.
            
        Returns:
            bool: Always returns True for testing purposes.

        """
        _ = username  # Use the argument to avoid linting error
        _ = password
        return True
        
    def authenticate(self, username: str, access_token: str) -> bool:
        """Authenticate using OAuth access token.
        
        Args:
            username: The email address to authenticate.
            access_token: The OAuth access token.
            
        Returns:
            bool: Always returns True for testing purposes.

        """
        _ = username
        _ = access_token
        return True
        
    def logout(self) -> None:
        """Terminate the current session."""
        
    def get_emails(self, query: str) -> list[dict]:
        """Retrieve emails matching the query.
        
        Args:
            query: The search query string.
            
        Returns:
            list[dict]: Empty list for testing purposes.

        """
        _ = query
        return []
        
    def get_email_content(self, email_id: str) -> dict:
        """Get the content of a specific email.
        
        Args:
            email_id: The ID of the email to retrieve.
            
        Returns:
            dict: Empty dictionary for testing purposes.

        """
        _ = email_id
        return {}
        
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send an email to the specified recipient.
        
        Args:
            to: The recipient's email address.
            subject: The email subject.
            body: The email body content.
            
        Returns:
            bool: Always returns True for testing purposes.

        """
        _ = to
        _ = subject
        _ = body
        return True
        
    def mark_as_read(self, email_id: str) -> bool:
        """Mark an email as read.
        
        Args:
            email_id: The ID of the email to mark as read.
            
        Returns:
            bool: Always returns True for testing purposes.

        """
        _ = email_id
        return True
        
    def detects_spam_email(self, email_id: str) -> bool:
        """Check if an email is spam.
        
        Args:
            email_id: The ID of the email to check.
            
        Returns:
            bool: Always returns False for testing purposes.

        """
        _ = email_id
        return False
        
    def unsubscribe_from_email_sender(self, email_id: str) -> bool:
        """Unsubscribe from the sender of an email.
        
        Args:
            email_id: The ID of the email whose sender to unsubscribe from.
            
        Returns:
            bool: Always returns True for testing purposes.

        """
        _ = email_id
        return True


def test_interface_definition() -> None:
    """Test that the interface is properly defined."""
    # Test that we can't instantiate the abstract class directly
    with pytest.raises(TypeError):
        GmailClientInterface()  # type: ignore[abstract]


def test_mock_implementation() -> None:
    """Test that our mock implementation works correctly."""
    client = MockGmailClient()
    
    # Test connection
    assert client.connect() is True
    
    # Test login
    assert client.login("test@example.com", "password") is True
    
    # Test authentication
    assert client.authenticate("test@example.com", "token") is True
    
    # Test logout (should not raise any exceptions)
    client.logout()
    
    # Test email operations
    assert client.get_emails("query") == []
    assert client.get_email_content("123") == {}
    assert client.send_email("to@example.com", "Subject", "Body") is True
    assert client.mark_as_read("123") is True
    assert client.detects_spam_email("123") is False
    assert client.unsubscribe_from_email_sender("123") is True


def test_interface_method_signatures() -> None:
    """Test that the interface methods have the correct signatures."""
    # Get all abstract methods
    abstract_methods = GmailClientInterface.__abstractmethods__
    
    # Verify all required methods are present
    required_methods = {
        "connect",
        "login",
        "authenticate",
        "logout",
        "get_emails",
        "get_email_content",
        "send_email",
        "mark_as_read",
        "detects_spam_email",
        "unsubscribe_from_email_sender",
    }
    
    assert abstract_methods == required_methods
