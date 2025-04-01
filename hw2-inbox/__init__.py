from typing import List, Dict
from abc import ABC, abstractmethod

class GmailClient(ABC):
    """
    Interface definition for a Gmail-based email client.
    This interface specifies core functionalities for email management including
    connection handling, authentication, and email operations.
    """
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Initialize a connection to the Gmail service.
        
        Returns:
            bool: True if the connection is successfully established, False otherwise.
        """
        pass
        
    @abstractmethod
    def login(self, username: str, password: str) -> bool:
        """
        Authenticate user credentials with the Gmail service.
        
        Args:
            username (str): The user's Gmail address.
            password (str): The user's password.
        
        Returns:
            bool: True if the login is successful, False otherwise.
        """
        pass
        
    @abstractmethod
    def authenticate(self, username: str, access_token: str) -> bool:
        """
        Authenticate using OAuth 2.0 access token.
        
        Args:
            username (str): The user's Gmail address.
            access_token (str): The OAuth access token.
        
        Returns:
            bool: True if the authentication is successful, False otherwise.
        """
        pass
        
    @abstractmethod
    def logout(self) -> None:
        """
        Terminate the current Gmail session.
        """
        pass
        
    @abstractmethod
    def get_emails(self, query: str) -> List[Dict]:
        """
        Retrieve emails matching the specified query criteria.
        
        Args:
            query (str): SQL query string for filtering emails.
        
        Returns:
            List[Dict]: A list of dictionaries containing email metadata such as
                       subject, sender, snippet, etc.
        """
        pass
        
    @abstractmethod
    def get_email_content(self, email_id: str) -> Dict:
        """
        Retrieve the complete content of a specified email.
        
        Args:
            email_id (str): Unique identifier of the email to be fetched.
        
        Returns:
            Dict: A dictionary containing detailed information about the email
                 (e.g., headers, body, attachments).
        """
        pass
        
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """
        Compose and send an email to the specified recipient.
        
        Args:
            to (str): The recipient's email address.
            subject (str): The subject line of the email.
            body (str): The content/body of the email.
        
        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        pass

    @abstractmethod
    def mark_as_read(self, email_id: str) -> bool:
        """
        Update the read status of a specified email.
        
        Args:
            email_id (str): Unique identifier of the email to be marked as read.
        
        Returns:
            bool: True if the email was marked as read successfully, False otherwise.
        """
        pass

    @abstractmethod
    def detects_spam_email(self, email_id: str) -> bool:
        """
        Evaluate an email for spam characteristics using content and metadata analysis.
        
        Args:
            email_id (str): Unique identifier of the email to be analyzed.
        
        Returns:
            bool: True if the email is identified as spam, False if the email is not spam.
        """
        pass

    @abstractmethod
    def unsubscribe_from_email_sender(self, email_id: str) -> bool:
        """
        Opt out of future communications from the specified email sender.
        
        Args:
            email_id (str): Unique identifier of the email whose sender to unsubscribe from.
        
        Returns:
            bool: True if successfully unsubscribed from the sender, False if the unsubscribe operation failed.
        """
        pass