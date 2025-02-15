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