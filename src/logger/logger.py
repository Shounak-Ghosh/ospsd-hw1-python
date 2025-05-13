"""Logger module for tracking operations."""

from datetime import datetime, timezone
from typing import List


class Logger:
    """Logger class for tracking operations."""

    def __init__(self) -> None:
        """Initialize logger with empty history."""
        self.history: List[str] = []

    def log_operation(self, operation: str) -> None:
        """Log an operation with timestamp.

        Args:
            operation: The operation to log

        """
        timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{timestamp}] {operation}")

    def get_history(self) -> List[str]:
        """Get the history of operations.

        Returns:
            List of logged operations with timestamps

        """
        return self.history