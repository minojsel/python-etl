"""
Logger Decorator to allow for better logging of all functions (Logging Level: Info).
Also catches any exceptions and logs them as an exception (Logging Level: Error).
"""
import logging
from functools import wraps

log = logging.getLogger(__name__)

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.info(f"Calling {func.__name__} with args {args} and kwargs {kwargs}")
            result = func(*args, **kwargs)
            logging.info(f"{func.__name__} execution completed")
            return result
        except Exception as e:
            log.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise e

    return wrapper