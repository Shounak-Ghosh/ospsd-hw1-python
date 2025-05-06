# ospsd-hw1-python
Open Source Professional Software Development hw1: Creating a template Python CI/CD repository

This repository provides a foundation for Python-based projects with integrated CI/CD pipelines, testing frameworks, static analysis, and code formatting. Below are specific instructions on how to utilize this template.

## Features
- **CI/CD Pipeline**: Integrated with CircleCI to automate testing, static analysis, and code coverage reporting
- **Static Analysis**: Uses `ruff` for code formatting and linting and `mypy` for static type checking to ensure code quality
- **Code Formatting**: Maintains consistent code style
- **Testing Framework**: Uses `pytest` for unit and integration tests
- **Components**: Includes `SpamDetector` with corresponding tests
- **Code Coverage**: Generates code coverage reports

## Getting Started
### Requirements
- Python 3.x
- CircleCI account
- GitHub repository

### Setup/Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/Shounak-Ghosh/ospsd-hw1-python.git
    cd ospsd-hw1-python
    ```

2. Install `uv`:
   - **MacOS and Linux**:
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - **Windows**:
     ```bash
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

3. Create and activate a virtual environment (`deactivate` to exit):
    ```bash
    uv venv
    source .venv/bin/activate  # macOS/Linux
    .venv\Scripts\activate     # Windows
    ```

4. Install dependencies (development dependencies are optional):
    ```bash
    uv sync
    uv sync --extra dev 
    ```

### Executing Tests
Make sure that development dependencies are installed.

1. **Static Analysis Tests (Linter checks)**:
    ```bash
    uv run ruff check .
    uv run mypy .
    ```

2. **Unit Tests**:
    ```bash
    uv run pytest hw2_tests/src/hw2_tests/test_spam_detector.py -v
    ```

3. **Unit Test Coverage Reports**:
    ```bash
    uv run pytest \
              --cov=hw2_inbox_impl \
              --cov=integration \
              --cov-report=html \
              --cov-report=xml \
              --cov-report=term-missing
    ```

4. **Integration Tests**:
    ```bash
    uv run pytest hw2_tests/src/hw2_tests/test_integration.py -v
    ```

### CircleCI Links
[CircleCI Success](https://app.circleci.com/pipelines/circleci/2EVebjbqRx5Qx95NT3zacE/9QkZ1CbHsQnVrG2Rq1GqqR/56/workflows/b36bd302-2794-4e2c-8059-c145990d9c61)

### Additional Notes
- The `SpamDetector` component has been added to analyze emails for spam using AI-based models. Mock implementations are provided for testing purposes.
- Mock AI clients (`MockAIClient` and `ErrorAIClient`) are used in integration tests to simulate AI behavior and error handling.
- Ensure that the `start_new_session` method in mock AI clients properly handles `user_id` and `model` arguments for compatibility with the `SpamDetector`.
