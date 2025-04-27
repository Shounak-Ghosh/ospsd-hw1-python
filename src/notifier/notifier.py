"""Notifier module for threshold-based alerts."""

class Notifier:
    """A class to handle threshold-based notifications."""

    def __init__(self, threshold: float) -> None:
        """Initialize notifier with a threshold value.

        Args:
            threshold: The threshold value for triggering notifications

        """
        self.threshold = threshold

    def send_notification(self, result: float) -> str:
        """Check if result exceeds threshold and send appropriate notification.

        Args:
            result: The value to check against the threshold

        Returns:
            A notification message based on the comparison

        """
        if result > self.threshold:
            return f"Alert! Result {result} exceeds threshold {self.threshold}"
        return "No alert needed"
