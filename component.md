# Components Documentation

This section provides an overview of the components in the `src/components/` directory. Each component is designed to perform a specific function and is tested with unit, integration, and end-to-end tests. Each component is a separate UV package with its own dependencies and configuration.

## Directory Structure
```
/ospsd-hw1-python
├── .circleci/
│   └── config.yml
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
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
│   └── _init_.py
├── test-results/
│   └── report.html
├── tests/
│   ├── end_to_end/
│   │   ├── _init_.py
│   │   └── test_e2e.py
│   ├── integration/
│   │   ├── _init_.py
│   │   ├── test_calc_logger_integration.py
│   │   └── test_calc_notifier_integration.py
│   └── _init_.py
├── .gitignore
├── component.md
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## 1. **Calculator**
### Description
The `Calculator` component performs basic arithmetic operations, such as addition, subtraction, and multiplication.

### Location
- File: `src/calculator/calculator.py`

### Methods
- **`add(a: float, b: float) -> float`**
  Adds two inputs and returns the result.

- **`subtract(a: float, b: float) -> float`**
  Subtracts the second input from the first input and returns the result.  

- **`multiply(a: float, b: float) -> float`**
  Multiplies two inputs and returns the result.

- **`divide(a: float, b: float) -> float`**
  Divides the first input by the second input and returns the result.

### Unit Tests
- File: `src/calculator/test_calculator.py`
- Tests:
  - `test_add`: Verifies the `add` method.
  - `test_subtract`: Verifies the `subtract` method.
  - `test_multiply`: Verifies the `multiply` method.
  - `test_divide`: Verifies the `divide` method.

---

## 2. **Logger**

### Description
The `Logger` component keeps track of operations performed by the calculator and stores them in a log (along with the timestamp of each operation).

### Location
- File: `src/logger/logger.py`
- Class: `OperationLogger`

### Methods
- **`log_operation(operation: str) -> None`**
  Logs a message.
- **`get_history() -> list[str]`**
  Returns list containing history of operations.

### Unit Tests
- File: `src/logger/test_logger.py`
- Tests:
  - `test_log_operation`: Verifies the `log_operation` method.

---

## 3. **Notifier**

### Description
The `Notifier` component sends an alert when the result of a `Calculator` operation exceeds a specified threshold.

### Location
- File: `src/notifier/notifier.py`
- Class: `Notifier`

### Methods
- **`send_notification(result: float) -> str`**  
  Sends a notification if the input result is over the threshold.

### Unit Tests
- File: `src/notifier/test_notifier.py`
- Tests:
  - `test_send_notification`: Verifies the `send_notification` method.

---

## Integration Tests

### Calculator and Logger
- File: `tests/integration/test_calc_logger_integration.py`
- Tests:
  - Verifies that `Calculator` operations are logged by the `Logger`.

### Calculator and Notifier
- File: `tests/integration/test_calc_notifier_integration.py`
- Tests:
  - Verifies that `Calculator` operations trigger the `Notifier` when a threshold is exceeded.

## End-to-End Tests

### Calculator -> Logger -> Notifier
- File: `tests/end_to_end/test_e2e.py`
- Tests:
  - Verifies the workflow from component to component:  
    1. Perform a calculation using the `Calculator`.  
    2. Log the operation using the `Logger`.  
    3. Send a notification using the `Notifier` if the result exceeds a threshold.
