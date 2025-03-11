# ospsd-hw1-python
Open Source Professional Software Development hw1: Creating a template Python CI/CD repository

This repository provides a foundation for Python-based projects with integrated CI/CD pipelines, testing frameworks, static analysis, and code formatting. Below details specific instructions on how to utilize this template.

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

2. Install uv: \
   MacOS and Linux:
   ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
   Windows:
   ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
4. Install dependencies:
    uv pip install pytest pytest-cov ruff mypy coverage

### Executing Tests
1. Static analysis (using pytest, ruff, mypy, coverage)
    uv run ruff check
    uv run mypy src

2. Tests (using pytest) and Code Coverage:
   uv run pytest 

### CircleCI Link  
[CircleCI](https://app.circleci.com/pipelines/circleci/2EVebjbqRx5Qx95NT3zacE/9QkZ1CbHsQnVrG2Rq1GqqR/25/workflows/a2f416d1-16af-4a28-b80a-1837987580da)

### Linter error check offs: 
D203, D213. This is because they were conflicting with other restrictions.
