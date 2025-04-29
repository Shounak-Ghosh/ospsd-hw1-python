"""Integration test module for calculator and logger components."""

from src.calculator import add
from src.logger import OperationLogger

# Test constants
TEST_VALUE_A = 5
TEST_VALUE_B = 3

def test_calc_logger_integration() -> None:
    """Test integration between calculator and logger components."""
    logger = OperationLogger()
    result = add(TEST_VALUE_A, TEST_VALUE_B)
    logger.log_operation(f"{TEST_VALUE_A} + {TEST_VALUE_B} = {result}")
    
    history = logger.get_history()
    assert len(history) == 1
    assert f"{TEST_VALUE_A} + {TEST_VALUE_B} = {result}" in history[0]
