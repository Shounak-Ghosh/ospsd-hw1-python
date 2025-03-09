# Components
## Calculator
- Goal: To perform basic arithmetic operations
- Key attributes: n/a
- Functionalities:
    - add(a, b)
    - subtract(a, b)
    - multiply(a, b)

## Logger
- Goal: Keeps track of operations performed by the calculator and the timestamp of each operation
- Key attributes:
    - history: List[str] -> logs the history of operations performed by a calculator
- Functionalities:
    - log_operation(operation)
    - get_history()

## Notifier
- Goal: Sends notifications when a result exceeds a specified threshold
- Key attributes:
    - threshold: float -> sets the threshold
- Functionalities:
    - send_notification(result)

## Directory Structure
/ospsd-hw1-python
├── .circleci/
│   └── config.yml
├── src/
│   ├── calculator
│   │   ├── _init_.py
│   │   ├── calculator.py
│   │   ├── pyproject.toml
│   │   └── test_calculator.py
│   ├── logger
│   │   ├── _init_.py
│   │   ├── logger.py
│   │   ├── pyproject.toml
│   │   └── test_logger.py
│   ├── notifier
│   │   ├── _init_.py
│   │   ├── notifier.py
│   │   ├── pyproject.toml
│   │   └── test_notifier.py
│   └──_init_.py
├── test-results/
│   └──report.html
├── tests/
│   ├── end_to_end/
│   │   ├── _init_.py
│   │   └── test_e2e.py
│   ├── integration/
│   │   ├── _init_.py
│   │   ├── test_calc_logger_integration.py
│   │   └── test_calc_notifier_integration.py
│   └──_init_.py
├── .gitignore
├── component.md
├── LICENSE
├── pull_request_template.md
├── pyproject.toml
├── README.md
└── uv.lock