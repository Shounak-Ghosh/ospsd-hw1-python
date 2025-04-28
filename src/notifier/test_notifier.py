"""Test module for notifier operations."""

from .notifier import Notifier

# Test constants
THRESHOLD = 10
ABOVE_THRESHOLD = 15
BELOW_THRESHOLD = 5

def test_send_notification() -> None:
    """Test notification sending based on threshold.
    
    Tests:
        - Notification when value exceeds threshold
        - Notification when value is below threshold
    """
    notifier = Notifier(threshold=THRESHOLD)
    assert notifier.send_notification(ABOVE_THRESHOLD) == f"Alert! Result {ABOVE_THRESHOLD} exceeds threshold {THRESHOLD}"
    assert notifier.send_notification(BELOW_THRESHOLD) == "No alert needed"
