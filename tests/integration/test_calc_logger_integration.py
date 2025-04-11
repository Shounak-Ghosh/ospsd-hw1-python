from unittest.mock import MagicMock
from src.logger.logger import OperationLogger

def test_calc_logger_integration():
    # Create a mock calculator
    mock_calculator = MagicMock()
    mock_calculator.add.return_value = 8  # Mock the add method to return 8

    # Initialize logger
    logger = OperationLogger()

    # Use mocked calculator's add method
    result = mock_calculator.add(5, 3)
    logger.log_operation(f"5 + 3 = {result}")

    # Assertions
    history = logger.get_history()
    assert len(history) == 1
    assert "5 + 3 = 8" in history[0]

    # Verify that add was called with correct arguments
    mock_calculator.add.assert_called_once_with(5, 3)
