"""Calculator module providing basic arithmetic operations."""

# Error messages
DIVISION_BY_ZERO_ERROR = "Cannot divide by zero"

def add(a: float, b: float) -> float:
    """Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b

    """
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract second number from first number.

    Args:
        a: First number
        b: Second number

    Returns:
        Difference of a and b

    """
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of a and b

    """
    return a * b

def divide(a: float, b: float) -> float:
    """Divide first number by second number.

    Args:
        a: First number (dividend)
        b: Second number (divisor)

    Returns:
        Quotient of a divided by b

    Raises:
        ValueError: If b is zero

    """
    if b == 0:
        raise ValueError(DIVISION_BY_ZERO_ERROR)
    return a / b