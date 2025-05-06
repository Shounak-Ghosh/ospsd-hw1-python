# Components Documentation

This section provides an overview of the components in the `src/components/` directory. Each component is designed to perform a specific function and is tested with unit and integration tests.

## Directory Structure
```
/ospsd-hw1-python
├── .circleci/
│   └── config.yml
├── ai_conversation_client/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── cerebras_client.py
│   │   ├── cli.py
│   │   ├── example.py
│   │   ├── factory.py
│   │   ├── interface.py
│   │   └── mock_client/
│   ├── test-results/
│   │   └── coverage.xml
├── hw2_inbox_api/
│   ├── src/
│   │   ├── hw2_inbox_api/
│   │   │   └── __init__.py
│   ├── pyproject.toml
│   └── README.md
├── hw2_inbox_impl/
│   ├── src/
│   │   ├── hw2_inbox_impl/
│   │   │   ├── __init__.py
│   │   │   ├── constants.py
│   │   │   └── gmail_client.py
│   └── pyproject.toml
├── hw2_tests/
│   ├── src/
│   │   ├── hw2_tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_hw2_inbox.py
│   │   │   ├── test_integration.py
│   │   │   └── test_spam_detector.py
│   └── pyproject.toml
├── integration/
│   ├── src/
│   │   ├── integration/
│   │   │   ├── __init__.py
│   │   │   ├── a.py
│   │   │   ├── constant.py
│   │   │   └── integration.py
│   ├── pyproject.toml
│   └── README.md
├── .gitignore
├── component.md
├── LICENSE
├── pull_request_template.md
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## 1. **SpamDetector**

### Description
The `SpamDetector` component analyzes emails for spam using AI-based models. It integrates with AI clients to classify emails and generate spam detection reports.

### Location
- File: `integration/src/integration/spam_detector.py`
- Class: `SpamDetector`

### Methods
- **`detect_spam(output_csv: str | None = None, max_emails: int | None = None) -> None`**
  Analyzes emails for spam and saves the results to a CSV file.
- **`analyze_email(session_id: str, email: dict[str, Any]) -> float`**
  Analyzes a single email and returns the percentage likelihood of it being spam.

### Unit Tests
- File: `hw2_tests/src/hw2_tests/test_spam_detector.py`
- Tests:
  - `test_detect_spam`: Verifies the `detect_spam` method.
  - `test_analyze_email`: Verifies the `analyze_email` method.

---

## Integration Tests

### SpamDetector
- File: `hw2_tests/src/hw2_tests/test_integration.py`
- Tests:
  - Verifies that the `SpamDetector` integrates with AI clients and handles errors gracefully.
