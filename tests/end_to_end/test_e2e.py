"""End-to-end tests for the calculator system.

Tests the integration between calculator, logger, and notifier components.
"""

from src.calculator import add
from src.logger.logger import OperationLogger
from src.notifier.notifier import Notifier


def test_end_to_end() -> None:
    """Test complete workflow of calculator with logging and notifications.
    
    Tests:
        - Adding numbers
        - Logging the operation
        - Notifying based on result threshold
    """
    logger = OperationLogger()
    notifier = Notifier(threshold=10)
    result = add(5, 3)
    logger.log_operation(f"{5} + {3} = {result}")
    notification = notifier.send_notification(result)

    # Assertions for E2E flow.
    history = logger.get_history()

    assert len(history) == 1
    assert "5 + 3 = 8" in history[0]

    assert notification == "Alert! Result 8 exceeds threshold 10"
