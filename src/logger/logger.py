"""Logger module for tracking operations with timestamps."""

from datetime import datetime, timezone


class OperationLogger:
    """A class to log and track operations with timestamps."""

    def __init__(self) -> None:
        """Initialize an empty operation history."""
        self.history: list[str] = []

    def log_operation(self, operation: str) -> None:
        """Log an operation with current timestamp.

        Args:
            operation: The operation to log

        """
        timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{operation} @ {timestamp}")

    def get_history(self) -> list[str]:
        """Retrieve the history of logged operations.

        Returns:
            List of logged operations with timestamps

        """
        return self.history
