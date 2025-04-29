"""Logger module for tracking operations."""

from datetime import datetime, timezone


class OperationLogger:
    """Logger class for tracking calculator operations."""

    def __init__(self) -> None:
        """Initialize an empty operation history."""
        self.history: list[str] = []

    def log_operation(self, operation: str) -> None:
        """Log an operation with timestamp.
        
        Args:
            operation: The operation to log

        """
        timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{operation} @ {timestamp}")

    def get_history(self) -> list[str]:
        """Get the history of operations.
        
        Returns:
            List of logged operations with timestamps

        """
        return self.history
