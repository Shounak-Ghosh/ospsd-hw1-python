from . import add, subtract, multiply, divide
import pytest

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 1) == -1

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 5) == -5

def test_divide():
    # Test normal division
    assert divide(6, 3) == 2
    assert divide(5, 2) == 2.5
    
    # Test edge cases (negative numbers)
    assert divide(-6, 3) == -2
    assert divide(6, -3) == -2
    
    # Test division by zero
    try:
        divide(5, 0)
        assert False, "Expected ValueError when dividing by zero"
    except ValueError as e:
        assert str(e) == "Cannot divide by zero"

def test_edge_cases():
    # Extremely large numbers
    large_num = 1e308
    small_num = 1e-308
    
    # Addition with large numbers
    assert add(large_num, large_num) == large_num * 2
    
    # Subtraction with large numbers
    assert subtract(large_num, large_num) == 0
    
    # Multiplication with large numbers
    assert multiply(large_num, small_num) == large_num * small_num
    
    # Division with large numbers
    assert divide(large_num, small_num) == large_num / small_num
    
    # Floating-point precision tests
    assert add(0.1, 0.2) == pytest.approx(0.3)
    assert subtract(0.3, 0.1) == pytest.approx(0.2)
    
    # Multiplication precision
    assert multiply(0.1, 0.2) == pytest.approx(0.02)
    
    # Division precision
    assert divide(1.0, 3.0) == pytest.approx(0.3333333333333333)

def test_extreme_values():
    import math
    
    # Test infinity handling
    assert add(math.inf, math.inf) == math.inf
    assert subtract(math.inf, math.inf) != math.inf  # Should result in NaN or undefined behavior
    
    # Test NaN handling
    nan = math.nan
    result = add(nan, nan)
    
    # Check if result is NaN (NaN != NaN in Python)
    assert math.isnan(result)
