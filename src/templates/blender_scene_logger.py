"""Logging setup for Blender scene generation."""

import logging
import os
import traceback
from datetime import datetime


def setup_logging(log_path: str = None):
    """Setup structured logging for debugging and error tracking.
    
    Args:
        log_path: Optional custom log file path
        
    Returns:
        Logger instance
    """
    log_format = '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    
    logger = logging.getLogger('blender_scene')
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    logger.handlers = []
    
    # File handler
    try:
        if log_path is None:
            log_path = "/Users/admir/ai/Cube/logs/blender_scene.log"
            
        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        fh = logging.FileHandler(log_path, 'a')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(log_format))
        logger.addHandler(fh)
    except Exception as e:
        pass  # File logging optional
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(ch)
    
    return logger


def log_error_to_file(error_msg: str, error_log_path: str, context: str = "", exception: Exception = None):
    """Log error to file for debugging.
    
    Args:
        error_msg: Error message
        error_log_path: Path to error log file
        context: Additional context
        exception: Exception object (optional)
    """
    try:
        timestamp = datetime.now().isoformat()
        
        # Ensure error log directory exists
        os.makedirs(os.path.dirname(error_log_path), exist_ok=True)
        
        with open(error_log_path, 'a') as f:
            f.write(f"{timestamp}: [{context}] {error_msg}\n")
            if exception:
                f.write(f"Exception: {type(exception).__name__}: {str(exception)}\n")
                f.write(traceback.format_exc())
                f.write("\n")
    except Exception:
        pass  # Error logging should not fail


def safe_operation(operation_name: str, func, logger, error_log_path: str, *args, **kwargs):
    """Safely execute an operation with error handling.
    
    Args:
        operation_name: Name of the operation
        func: Function to execute
        logger: Logger instance
        error_log_path: Path to error log file
        *args, **kwargs: Arguments to pass to func
        
    Returns:
        Result of func execution
        
    Raises:
        Exception: If operation fails
    """
    try:
        logger.debug(f"Executing: {operation_name}")
        result = func(*args, **kwargs)
        logger.debug(f"Completed: {operation_name}")
        return result
    except Exception as e:
        logger.error(f"Failed: {operation_name} - {e}")
        log_error_to_file(str(e), error_log_path, operation_name, e)
        raise

