"""Notifier module for threshold-based alerts."""

class Notifier:
    """Notifier class for threshold-based alerts."""

    def __init__(self, threshold: float) -> None:
        """Initialize notifier with a threshold.

        Args:
            threshold: The threshold value for alerts

        """
        self.threshold = threshold

    def send_notification(self, result: float) -> str:
        """Send notification if result exceeds threshold.

        Args:
            result: The value to check against threshold

        Returns:
            Alert message if threshold is exceeded

        """
        if result > self.threshold:
            return f"Alert! Result {result} exceeds threshold {self.threshold}"
        return "No alert needed"
