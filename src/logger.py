from datetime import datetime
from typing import List

class OperationLogger:
    def __init__(self):
        self.history: List[str] = []

    def log_operation(self, operation: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{operation} @ {timestamp}")

    def get_history(self) -> List[str]:
        return self.history
