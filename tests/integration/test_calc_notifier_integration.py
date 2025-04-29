"""Integration test module for calculator and notifier components."""

from src.calculator import add
from src.logger import OperationLogger
from src.notifier import Notifier

# Test constants
TEST_THRESHOLD = 10
TEST_VALUE_A = 7
TEST_VALUE_B = 8

def test_logger_notifier_integration() -> None:
    """Test integration between calculator, logger, and notifier components."""
    logger = OperationLogger()
    notifier = Notifier(threshold=TEST_THRESHOLD)
    
    # Perform calculation
    result = add(TEST_VALUE_A, TEST_VALUE_B)
    logger.log_operation(f"{TEST_VALUE_A} + {TEST_VALUE_B} = {result}")
    
    # Check notification
    notification = notifier.send_notification(result)
    
    # Verify results
    history = logger.get_history()
    assert len(history) == 1
    assert f"{TEST_VALUE_A} + {TEST_VALUE_B} = {result}" in history[0]
    assert notification == f"Alert! Result {result} exceeds threshold {TEST_THRESHOLD}"
