"""End-to-end test module for the calculator application."""

from src.calculator import add
from src.logger import OperationLogger
from src.notifier import Notifier

# Test constants
TEST_THRESHOLD = 10
TEST_VALUE_A = 5
TEST_VALUE_B = 3

def test_end_to_end() -> None:
    """Test the complete workflow of calculator, logger, and notifier."""
    logger = OperationLogger()
    notifier = Notifier(threshold=TEST_THRESHOLD)
    
    # Perform calculation
    result = add(TEST_VALUE_A, TEST_VALUE_B)
    
    # Log operation
    logger.log_operation(f"{TEST_VALUE_A} + {TEST_VALUE_B} = {result}")
    
    # Check notification
    notification = notifier.send_notification(result)
    
    # Verify results
    history = logger.get_history()
    assert len(history) == 1
    assert f"{TEST_VALUE_A} + {TEST_VALUE_B} = {result}" in history[0]
    assert notification == "No alert needed"
