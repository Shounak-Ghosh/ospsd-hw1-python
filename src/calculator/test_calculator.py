"""Test module for calculator operations."""

from . import add, multiply, subtract

# Test constants
TEST_SUM = 5
TEST_DIFF = 2
TEST_PRODUCT = 6
TEST_NEG_PRODUCT = -5

def test_add() -> None:
    """Test addition operation."""
    assert add(2, 3) == TEST_SUM
    assert add(-1, 1) == 0

def test_subtract() -> None:
    """Test subtraction operation."""
    assert subtract(5, 3) == TEST_DIFF
    assert subtract(0, 1) == -1

def test_multiply() -> None:
    """Test multiplication operation."""
    assert multiply(2, 3) == TEST_PRODUCT
    assert multiply(-1, 5) == TEST_NEG_PRODUCT
