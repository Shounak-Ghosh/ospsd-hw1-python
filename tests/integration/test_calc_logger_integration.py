"""Integration tests for calculator and logger components."""

from src.calculator import add
from src.logger.logger import OperationLogger


def test_calc_logger_integration() -> None:
    """Test integration between calculator and logger.
    
    Tests:
        - Performing calculation
        - Logging the operation result
        - Verifying log contents
    """
    logger = OperationLogger()
    result = add(5, 3)
    logger.log_operation(f"5 + 3 = {result}")
    
    history = logger.get_history()
    assert len(history) == 1
    assert "5 + 3 = 8" in history[0]
