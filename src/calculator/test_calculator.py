"""Test module for calculator operations."""

from . import add, multiply, subtract


def test_add() -> None:
    """Test addition operation."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract() -> None:
    """Test subtraction operation."""
    assert subtract(5, 3) == 2
    assert subtract(0, 1) == -1

def test_multiply() -> None:
    """Test multiplication operation."""
    assert multiply(2, 3) == 6
    assert multiply(-1, 5) == -5