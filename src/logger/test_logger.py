"""Test module for logger operations."""

from .logger import Logger


def test_log_operation() -> None:
    """Test logging an operation."""
    logger = Logger()
    logger.log_operation("2 + 3 = 5")
    history = logger.get_history()
    assert len(history) == 1
    assert "2 + 3 = 5" in history[0]
