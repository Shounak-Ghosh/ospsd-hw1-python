"""Test module for notifier operations."""

from .notifier import Notifier

# Test constants
TEST_THRESHOLD = 10
TEST_VALUE = 15

def test_notification_threshold_exceeded() -> None:
    """Test notification when threshold is exceeded."""
    notifier = Notifier(threshold=TEST_THRESHOLD)
    expected_message = (
        f"Alert! Result {TEST_VALUE} exceeds threshold {TEST_THRESHOLD}"
    )
    assert notifier.send_notification(TEST_VALUE) == expected_message
    assert notifier.send_notification(5) == "No alert needed"