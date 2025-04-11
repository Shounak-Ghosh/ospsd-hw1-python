# Gmail Client Interface
This interface specifies the core functionality of the Gmail Client, encompassing connection management, authentication, and email operations. The client is designed to integrate seamlessly with other team projects including AI Conversation Client, Chat Client, and Issue Tracker Client.

---

## Project Overview
The project implements a Gmail client interface with the following core capabilities:
- Establish connection with Gmail servers
- User authentication via email/password
- OAuth token-based authentication
- Email composition and sending
- Spam detection and management
- Email subscription management

The following features are explicitly **out-of-scope**:
- Mailbox-specific operations
- ... 


## Interface Definition

1. ```connect(self) -> bool```
   - **Description**: Initialize a connection to the Gmail service.
   - **Parameters**:
     - **self**
   - **Returns**:
     - `True` if the connection is successfully established.
     - `False` otherwise.

2. ```login(self, username: str, password: str) -> bool```
   - **Description**: Authenticate user credentials with the Gmail service.
   - **Parameters**:
     - **self**
     - **username** *(str)*: The user's Gmail address.
     - **password** *(str)*: The user's password.
   - **Returns**:
     - `True` if the login is successful.
     - `False` otherwise.

3. ```authenticate(self, username: str, access_token: str) -> bool```
   - **Description**: Authenticate using OAuth 2.0 access token.
   - **Parameters**:
     - **self**
     - **username** *(str)*: The user's Gmail address.
     - **access_token** *(str)*: The OAuth access token.
   - **Returns**:
     - `True` if the authentication is successful.
     - `False` otherwise.

4. ```logout(self) -> None```
   - **Description**: Terminate the current Gmail session.
   - **Parameters**:
     - **self**
   - **Returns**:  
     - Nothing (`None`). This method terminates the active session.

5. ```get_emails(self, query: str) -> List[Dict]```
   - **Description**: Retrieve emails matching the specified query criteria.
   - **Parameters**:
     - **self**
     - **query** *(str)*: SQL query string
   - **Returns**:
     - A `List[Dict]` where each dictionary contains metadata such as 
       `subject`, `sender`, `snippet`, etc.

6. ```get_email_content(self, email_id: str) -> Dict```
   - **Description**: Retrieve the complete content of a specified email.
   - **Parameters**:
     - **self**
     - **email_id** *(str)*: Unique identifier of the email to be fetched.
   - **Returns**:
     - A `Dict` containing detailed information about the email (e.g., headers, body, attachments).

7. ```send_email(self, to: str, subject: str, body: str) -> bool```
   - **Description**: Compose and send an email to the specified recipient.
   - **Parameters**:
     - **self**
     - **to** *(str)*: The recipient's email address.
     - **subject** *(str)*: The subject line of the email.
     - **body** *(str)*: The content/body of the email.
   - **Returns**:
     - `True` if the email was sent successfully.
     - `False` otherwise.

8. ```mark_as_read(self, email_id: str) -> bool```
   - **Description**: Update the read status of a specified email.
   - **Parameters**:
     - **self**
     - **email_id** *(str)*: Unique identifier of the email to be marked as read.
   - **Returns**:
     - `True` if the email was marked as read successfully.
     - `False` otherwise.

9. ```detects_spam_email(self, email_id: str) -> bool```
   - **Description**: Evaluate an email for spam characteristics using content and metadata analysis.
   - **Parameters**:
     - **self**
     - **email_id** *(str)*: Unique identifier of the email to be analyzed.
   - **Returns**:
     - `True` if the email is identified as spam.
     - `False` if the email is not spam.

10. ```unsubscribe_from_email_sender(self, email_id: str) -> bool```
    - **Description**: Opt out of future communications from the specified email sender.
    - **Parameters**:
      - **self**
      - **email_id** *(str)*: Unique identifier of the email whose sender to unsubscribe from.
    - **Returns**:
      - `True` if successfully unsubscribed from the sender.
      - `False` if the unsubscribe operation failed.