import logging
import sys
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance with the specified module name.
    Usage:
        from app.core.logger import get_logger
        logger = get_logger(__name__)
    """
    return logging.getLogger(name)
