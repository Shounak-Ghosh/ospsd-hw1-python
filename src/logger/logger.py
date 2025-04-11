from datetime import datetime

class OperationLogger:
    def __init__(self) -> None:
        """Initializes the OperationLogger with an empty history list.
        """
        self.history: list[str] = []

    def log_operation(self, operation: str) -> None:
        """Logs an operation with a timestamp.

        Args:
            operation (str): The operation description to be logged.

        Returns:
            None

        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{operation} @ {timestamp}")

    def get_history(self) -> list[str]:
        """Returns the logged history.

        Returns:
            list[str]: The list of logged operations.

        """
        return self.history
