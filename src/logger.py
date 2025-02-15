from typing import List
import datetime

class OperationLogger:
    def __init__(self):
        self.history: List[str] = []
    
    def log_operation(self, operation: str):
        self.history.append(f"{operation} @ {datetime.now()}")
