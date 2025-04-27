"""Calculator module providing basic arithmetic operations."""

def add(a: float, b: float) -> float:
    """Add two numbers together.

    Args:
        a: First number to add
        b: Second number to add

    Returns:
        The sum of a and b

    """
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract second number from first number.

    Args:
        a: Number to subtract from
        b: Number to subtract

    Returns:
        The difference between a and b

    """
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers together.

    Args:
        a: First number to multiply
        b: Second number to multiply

    Returns:
        The product of a and b

    """
    return a * b

def divide(a: float, b: float) -> float:
    """Divide first number by second number.

    Args:
        a: Number to divide
        b: Number to divide by

    Returns:
        The quotient of a divided by b

    Raises:
        ValueError: If attempting to divide by zero

    """
    division_error = "Cannot divide by zero"
    if b == 0:
        raise ValueError(division_error)
    return a / b
