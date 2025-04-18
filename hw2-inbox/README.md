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
- Mailbox-specific operations (e.g., folder management)
- UI integration or rendering logic
- Offline caching or synchronization

## Setup Instructions
Create and activate a virtual environment
```
uv venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
```
Install  packages and dependencies
```
uv pip install -e .        # Install the full workspace
uv add --dev pytest pytest-mock pytest-cov mypy ruff
```
Run tests
```
pytest
```
Run Type Checker
```
mypy interface/ implementation/
```
Run Linter
```
ruff check interface/ implementation/
```

