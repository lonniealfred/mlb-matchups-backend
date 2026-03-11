# app/utils/logging.py

import logging
from logging.handlers import RotatingFileHandler


# ---------------------------------------------------------
# Base configuration
# ---------------------------------------------------------

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | "
    "%(message)s"
)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT
)


# ---------------------------------------------------------
# Optional file logging (disabled by default)
# ---------------------------------------------------------

def _create_file_handler():
    handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=2_000_000,   # 2 MB
        backupCount=3
    )
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return handler


FILE_LOGGING_ENABLED = False

if FILE_LOGGING_ENABLED:
    file_handler = _create_file_handler()
    logging.getLogger().addHandler(file_handler)


# ---------------------------------------------------------
# Public helper
# ---------------------------------------------------------

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with consistent formatting.
    """
    return logging.getLogger(name)
