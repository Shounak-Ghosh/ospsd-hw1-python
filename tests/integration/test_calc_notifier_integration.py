"""Integration tests for calculator and notifier."""

from src.calculator.calculator import add
from src.logger import Logger
from src.notifier.notifier import Notifier


def test_calc_notifier_integration() -> None:
    """Test integration between calculator and notifier."""
    # Setup
    logger = Logger()
    notifier = Notifier(threshold=7)  # Alert if result > 7

    # Perform operation
    result = add(5, 10)  # 5 + 10 = 15
    logger.log_operation(f"5 + 10 = {result}")
    notification = notifier.send_notification(result)

    # Verify results
    history = logger.get_history()
    assert len(history) == 1
    assert "5 + 10 = 15" in history[0]
    assert notification == "Alert! Result 15 exceeds threshold 7"
