"""
Utility functions for RAG agent implementation.

This module provides helper functions for logging, error handling,
and common operations used across the RAG pipeline.
"""

import logging
from typing import Any, Callable, Optional
from functools import wraps
import time


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0
) -> Callable:
    """
    Decorator for retrying functions with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds before first retry
        backoff_factor: Multiplier for delay between retries
        
    Returns:
        Decorated function with retry logic
        
    Example:
        @retry_with_backoff(max_retries=3)
        def api_call():
            # API call that might fail
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}: {e}"
                    )
                    
                    if attempt < max_retries - 1:
                        logger.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                        delay *= backoff_factor
            
            logger.error(f"All {max_retries} attempts failed for {func.__name__}")
            raise last_exception
        
        return wrapper
    return decorator


def validate_input(value: Any, value_name: str, expected_type: type) -> None:
    """
    Validate input parameter type.
    
    Args:
        value: Value to validate
        value_name: Name of the parameter (for error messages)
        expected_type: Expected type of the value
        
    Raises:
        TypeError: If value is not of expected type
        ValueError: If value is None or empty
    """
    if value is None:
        raise ValueError(f"{value_name} cannot be None")
    
    if not isinstance(value, expected_type):
        raise TypeError(
            f"{value_name} must be of type {expected_type.__name__}, "
            f"got {type(value).__name__}"
        )
    
    # Additional validation for strings and collections
    if isinstance(value, str) and not value.strip():
        raise ValueError(f"{value_name} cannot be empty")
    
    if isinstance(value, (list, dict)) and len(value) == 0:
        raise ValueError(f"{value_name} cannot be empty")


def measure_time(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to measure
        
    Returns:
        Decorated function that logs execution time
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
        
        return result
    
    return wrapper


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Default value to return if denominator is zero
        
    Returns:
        Result of division or default value
    """
    try:
        if denominator == 0:
            logger.warning("Division by zero, returning default value")
            return default
        return numerator / denominator
    except Exception as e:
        logger.error(f"Error in division: {e}")
        return default


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length with suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length of output
        suffix: Suffix to add if text is truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
