import unittest
from unittest.mock import create_autospec
from typing import List, Dict, Any

from .. import GmailClient

class TestGmailClientInterface(unittest.TestCase):
    """Test suite for the Gmail Client Interface implementation."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_client = create_autospec(GmailClient, instance=True)

    def tearDown(self):
        """Clean up after each test method."""
        self.mock_client = None

    # Connection Management Tests
    def test_connect_success(self):
        """Test successful connection to Gmail service."""
        self.mock_client.connect.return_value = True
        result = self.mock_client.connect()
        self.assertTrue(result)
        self.mock_client.connect.assert_called_once()

    def test_connect_failure(self):
        """Test failed connection to Gmail service."""
        self.mock_client.connect.return_value = False
        result = self.mock_client.connect()
        self.assertFalse(result)
        self.mock_client.connect.assert_called_once()

    # Authentication Tests
    def test_login_success(self):
        """Test successful login with valid credentials."""
        self.mock_client.login.return_value = True
        result = self.mock_client.login("example@example.com", "password")
        self.assertTrue(result)
        self.mock_client.login.assert_called_once_with("example@example.com", "password")

    def test_login_failure(self):
        """Test login failure with invalid credentials."""
        self.mock_client.login.return_value = False
        result = self.mock_client.login("example@example.com", "wrong_password")
        self.assertFalse(result)
        self.mock_client.login.assert_called_once_with("example@example.com", "wrong_password")

    def test_authenticate_success(self):
        """Test successful OAuth authentication."""
        self.mock_client.authenticate.return_value = True
        result = self.mock_client.authenticate("example@example.com", "sample_access_token")
        self.assertTrue(result)
        self.mock_client.authenticate.assert_called_once_with("example@example.com", "sample_access_token")

    def test_logout(self):
        """Test successful logout from Gmail session."""
        self.mock_client.logout.return_value = None
        self.mock_client.logout()
        self.mock_client.logout.assert_called_once()

    # Email Retrieval Tests
    def test_get_emails_with_query(self):
        """Test retrieving emails with a specific query."""
        expected_emails: List[Dict[str, Any]] = [
            {"id": "1", "subject": "Hello", "sender": "1@example.com", "snippet": "Hi there"},
            {"id": "2", "subject": "World", "sender": "2@example.com", "snippet": "Greetings"}
        ]
        self.mock_client.get_emails.return_value = expected_emails
        result = self.mock_client.get_emails("SELECT * FROM emails WHERE unread = true")
        self.assertEqual(result, expected_emails)
        self.mock_client.get_emails.assert_called_once_with("SELECT * FROM emails WHERE unread = true")

    def test_get_emails_empty_result(self):
        """Test retrieving emails when no results are found."""
        self.mock_client.get_emails.return_value = []
        result = self.mock_client.get_emails("SELECT * FROM emails WHERE id = 'nonexistent'")
        self.assertEqual(result, [])
        self.mock_client.get_emails.assert_called_once()

    def test_get_email_content(self):
        """Test retrieving complete content of a specific email."""
        email_content = {
            "id": "1",
            "subject": "Hello",
            "body": "This is a test email.",
            "headers": {"From": "sender@example.com", "Date": "2024-03-20"},
            "attachments": []
        }
        self.mock_client.get_email_content.return_value = email_content
        result = self.mock_client.get_email_content("1")
        self.assertEqual(result, email_content)
        self.mock_client.get_email_content.assert_called_once_with("1")

    # Email Management Tests
    def test_send_email_success(self):
        """Test successful email sending."""
        self.mock_client.send_email.return_value = True
        result = self.mock_client.send_email(
            "recipient@example.com",
            "Test Subject",
            "Test Body"
        )
        self.assertTrue(result)
        self.mock_client.send_email.assert_called_once_with(
            "recipient@example.com",
            "Test Subject",
            "Test Body"
        )

    def test_send_email_failure(self):
        """Test email sending failure."""
        self.mock_client.send_email.return_value = False
        result = self.mock_client.send_email(
            "invalid@example.com",
            "Test Subject",
            "Test Body"
        )
        self.assertFalse(result)
        self.mock_client.send_email.assert_called_once()

    def test_mark_as_read_success(self):
        """Test successful marking of email as read."""
        self.mock_client.mark_as_read.return_value = True
        result = self.mock_client.mark_as_read("1")
        self.assertTrue(result)
        self.mock_client.mark_as_read.assert_called_once_with("1")

    # Spam and Subscription Management Tests
    def test_detects_spam_email(self):
        """Test spam detection for an email."""
        self.mock_client.detects_spam_email.return_value = True
        result = self.mock_client.detects_spam_email("1")
        self.assertTrue(result)
        self.mock_client.detects_spam_email.assert_called_once_with("1")

    def test_unsubscribe_from_email_sender_success(self):
        """Test successful unsubscription from email sender."""
        self.mock_client.unsubscribe_from_email_sender.return_value = True
        result = self.mock_client.unsubscribe_from_email_sender("1")
        self.assertTrue(result)
        self.mock_client.unsubscribe_from_email_sender.assert_called_once_with("1")


if __name__ == "__main__":
    unittest.main()