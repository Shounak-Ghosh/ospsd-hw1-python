# ospsd-hw1-python
Open Source Professional Software Development hw1: Creating a template Python CI/CD repository

This repository provides a foundation for Python-based projects with integrated CI/CD pipelines, testing frameworks, static analysis, and code formatting. Below details specific instructions on how to utilize this template.

## Features
- CI/CD Pipeline: Integrated with CircleCI to automate testing, static analysis, and code coverage reporting
- Static Analysis: Uses 'ruff' for code formatting and linting and 'mypy' for static type checking to ensure code quality
- Code Formatting: Maintains consistent code style
- Testing Framework: Uses 'pytest' for unit, integration, and end-to-end tests
- Components: 
  - Gmail Client: A Python implementation of a Gmail client with OAuth2 authentication
  - Email Management: Features for sending, receiving, and managing emails
  - Spam Detection: Basic spam detection functionality
  - Unsubscribe Support: Ability to unsubscribe from email senders
- Code Coverage: Generates code coverage reports

## Project Structure
- `hw2_inbox/`: Root package containing the Gmail client interface
- `hw2_inbox_impl/`: Implementation of the Gmail client
- `hw2_tests/`: Test suite for the Gmail client implementation

## Getting Started
### Requirements
- Python 3.x
- CircleCI account
- GitHub repository

### Setup/Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/Shounak-Ghosh/ospsd-hw1-python.git
    cd project-name

2. Install uv: \
MacOS and Linux:
   ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
   Windows:
   ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
3. Create and activate virtual environment (`deactivate` for exiting)
   ```
   uv venv
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate   # Windows
   ```

5. Install dependencies (development dependencies are optional):
    ```
    uv sync && uv sync --extra dev
    ```

### Executing Tests
Make sure that dev dependencies are installed. 
1. Static Analysis Tests (Linter checks)
    ```
    uv run ruff check .
    uv run mypy .
    ```
2. Unit Tests
    ```
    # ensure that you are outside the hw2_inbox package (cd ..)
    uv run pytest hw2_tests/src/hw2_tests/test_hw2_inbox.py --junitxml=test-results/pytest/junit.xml --html=test-results/report.html --self-contained-html

    ```
3. Unit test coverage reports
    ```
    # ensure that you are outside the hw2_inbox package
    uv run pytest --cov=hw2_inbox_impl --cov-report=html --cov-report=xml --cov-report=term-missing


    ```

### CircleCI Links 
[CircleCI Failure](https://app.circleci.com/pipelines/circleci/2EVebjbqRx5Qx95NT3zacE/9QkZ1CbHsQnVrG2Rq1GqqR/86/workflows/d9bc6b5a-6639-4a45-ae4c-d2908bbd4e7b)

[CircleCI Success](https://app.circleci.com/pipelines/circleci/2EVebjbqRx5Qx95NT3zacE/9QkZ1CbHsQnVrG2Rq1GqqR/85/workflows/62d8f317-e25b-460e-a315-f0f368bd42f0)