"""Integration tests for calculator and logger."""

from src.calculator.calculator import add
from src.logger import Logger


def test_calc_logger_integration() -> None:
    """Test integration between calculator and logger."""
    # Setup
    logger = Logger()

    # Perform operation
    result = add(5, 10)  # 5 + 10 = 15
    logger.log_operation(f"5 + 10 = {result}")

    # Verify results
    history = logger.get_history()
    assert len(history) == 1
    assert "5 + 10 = 15" in history[0]
