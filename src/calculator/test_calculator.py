"""Test module for calculator operations."""

from . import add, multiply, subtract

# Test constants
FIRST_NUMBER = 2
SECOND_NUMBER = 3
EXPECTED_SUM = 5
EXPECTED_DIFFERENCE = 2
EXPECTED_PRODUCT = 6
NEGATIVE_ONE = -1
ZERO = 0
ONE = 1
FIVE = 5
NEGATIVE_FIVE = -5

def test_add() -> None:
    """Test addition with positive and negative numbers."""
    assert add(FIRST_NUMBER, SECOND_NUMBER) == EXPECTED_SUM
    assert add(NEGATIVE_ONE, ONE) == ZERO

def test_subtract() -> None:
    """Test subtraction with various number combinations."""
    assert subtract(FIVE, SECOND_NUMBER) == EXPECTED_DIFFERENCE
    assert subtract(ZERO, ONE) == NEGATIVE_ONE

def test_multiply() -> None:
    """Test multiplication with positive and negative numbers."""
    assert multiply(FIRST_NUMBER, SECOND_NUMBER) == EXPECTED_PRODUCT
    assert multiply(NEGATIVE_ONE, FIVE) == NEGATIVE_FIVE
