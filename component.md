# Components Documentation

This section provides an overview of the components in the project. Each component is designed to perform specific Gmail-related functions and is tested with unit and integration tests. The project is organized into three main packages with their own dependencies and configuration.

## Directory Structure
```
/ospsd-hw1-python
├── .circleci/
│   └── config.yml
├── .github/
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── hw2_inbox_api/
│   ├── src/
│   │   └── hw2_inbox_api/
│   │       ├── __init__.py
│   ├── pyproject.toml
├── hw2_inbox_impl/
│   ├── src/
│   │   └── hw2_inbox_impl/
│   │       ├── __init__.py
│   │       ├── constants.py
│   │       ├── gmail_client.py
│   │       ├── py.typed
│   ├── pyproject.toml
├── hw2_tests/
│   ├── src/
│   │   └── hw2_tests/
│   │       ├── __init__.py
│   │       ├── test_hw2_inbox.py
│   ├── pyproject.toml
│   └── uv.lock
├── test-results/
│   ├── pytest/
│   │   └── junit.xml
│   └── report.html
├── .gitignore
├── LICENSE
├── README.md
├── component.md
├── coverage.xml
├── pull_request_template.md
├── pyproject.toml
└── uv.lock
```

---

## 1. **Gmail Client Interface**
### Description
The `GmailClientInterface` defines the contract for Gmail client implementations, specifying the required methods and their signatures.

### Location
- File: `hw2_inbox_api/src/hw2_inbox_api/__init__.py`

### Methods
- **`connect() -> bool`**
  Establishes connection to Gmail service.

- **`authenticate(email: str, token: str) -> bool`**
  Authenticates user with email and token.

- **`get_emails(query: str = "") -> list[dict]`**
  Retrieves emails matching the query.

- **`send_email(to: str, subject: str, body: str) -> bool`**
  Sends an email to the specified recipient.

- **`mark_as_read(email_id: str) -> bool`**
  Marks an email as read.

- **`detect_spam(email_id: str) -> bool`**
  Detects if an email is spam.

- **`unsubscribe_from_email_sender(email_id: str) -> bool`**
  Unsubscribes from the sender of an email.

---

## 2. **Gmail Client Implementation**

### Description
The `GmailClient` class implements the `GmailClientInterface`, providing concrete functionality for Gmail operations using the Gmail API and OAuth2 authentication.

### Location
- File: `hw2_inbox_impl/src/hw2_inbox_impl/gmail_client.py`
- Class: `GmailClient`

### Key Features
- OAuth2 Authentication
- Email Management
- Spam Detection
- Unsubscribe Support

### Dependencies
- google-api-python-client
- google-auth-oauthlib
- google-auth-httplib2

---

## 3. **Test Suite**

### Description
The test suite verifies the functionality of the Gmail client implementation against the interface requirements.

### Location
- File: `hw2_tests/src/hw2_tests/test_hw2_inbox.py`

### Test Categories
1. **Connection Tests**
   - Test successful connection
   - Test connection failure

2. **Authentication Tests**
   - Test successful authentication
   - Test authentication failure

3. **Email Operation Tests**
   - Test email retrieval
   - Test email sending
   - Test marking emails as read
   - Test spam detection
   - Test unsubscribe functionality

### Test Configuration
- Uses pytest for testing
- Includes mock objects for Gmail API
- Generates HTML and JUnit XML reports
- Integrates with CircleCI for continuous testing
