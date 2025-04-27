"""Test module for logger operations."""

from .logger import OperationLogger


def test_log_operation() -> None:
    """Test logging operations and history retrieval.
    
    Tests:
        - Logging a single operation
        - Verifying history length
        - Verifying operation content in history
    """
    logger = OperationLogger()
    logger.log_operation("2 + 3 = 5")
    assert len(logger.get_history()) == 1
    assert "2 + 3 = 5" in logger.get_history()[0]
