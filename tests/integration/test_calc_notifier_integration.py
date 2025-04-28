"""Integration tests for logger and notifier components."""

from src.logger.logger import OperationLogger
from src.notifier.notifier import Notifier


def test_logger_notifier_integration() -> None:
    """Test integration between logger and notifier.
    
    Tests:
        - Logging an operation
        - Checking notification threshold
        - Verifying notification message
    """
    logger = OperationLogger()
    notifier = Notifier(threshold=10)
    
    # Log an operation and check notification
    logger.log_operation("15 + 20 = 35")
    notification = notifier.send_notification(35)
    
    # Verify both logging and notification worked
    history = logger.get_history()
    assert len(history) == 1
    assert "15 + 20 = 35" in history[0]
    assert notification == "Alert! Result 35 exceeds threshold 10"
