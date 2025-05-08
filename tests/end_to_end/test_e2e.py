"""End-to-end tests for the calculator application."""

from src.calculator.calculator import add
from src.logger import Logger
from src.notifier.notifier import Notifier


def test_e2e_flow() -> None:
    """Test the complete flow of calculator operations."""
    # Setup
    logger = Logger()
    notifier = Notifier(threshold=10)  # Alert if result > 10

    # Perform operation
    result = add(5, 3)  # 5 + 3 = 8
    logger.log_operation(f"5 + 3 = {result}")
    notification = notifier.send_notification(result)

    # Verify results
    history = logger.get_history()
    assert len(history) == 1
    assert "5 + 3 = 8" in history[0]
    assert notification == "No alert needed"
