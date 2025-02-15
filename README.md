# ospsd-hw1-python
Open Source Professional Software Development hw1: Creating a template Python CI/CD repository

This repository provides a foundation for Python-based projects with integrated CI/CD pipelines, testing frameworks, static analysis, and code formatting.

## Features
- CI/CD Pipeline: Integrated with CircleCI to automate testing, static analysis, and code coverage reporting
- Static Analysis: Uses 'ruff' for code formatting and linting and 'mypy' for static type checking to ensure code quality
- Code Formatting: Maintains consistent code style
- Testing Framework: Uses 'pytest' for unit, integration, and end-to-end tests
- Components: 'Calculator', 'Logger', and 'Notifier', each with corresponding tests and documentation
- Code Coverage: Generates code coverage reports

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

2. Install uv:
    python -m pip install --upgrade pip
    pip install uv

3. Create virtual environment and run it:
    uv venv
    source .venv/bin/activate

4. Install dependencies:
    pip install pytest pytest-cov ruff mypy coverage

### Executing tests
1. Static analysis (using pytest, ruff, mypy, coverage)
    uv run ruff check
    uv run mypy src

2. Tests (using pytest)
    uv run pytest --cov=src --cov-report=xml --junitxml=test-results/results.xml -v

3. Code coverage
    uv run pytest --cov=src --cov-report=html -v