"""Main package initialization.

This module provides access to calculator operations,
logging functionality, and notification services.
"""

# Using calculator
from .calculator import add, divide, multiply, subtract

# Using logger
from .logger import OperationLogger

# Using notifier
from .notifier import Notifier

__all__ = [
    "Notifier",
    "OperationLogger",
    "add",
    "divide",
    "multiply",
    "subtract",
]
