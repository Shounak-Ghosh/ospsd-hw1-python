from datetime import datetime

class OperationLogger:
    def __init__(self) -> None:
        self.history: list[str] = []

    def log_operation(self, operation: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{operation} @ {timestamp}")

    def get_history(self) -> list[str]:
        return self.history
