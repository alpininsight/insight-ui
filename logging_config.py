"""Logging configuration for the demo application."""

import logging
import os

LOGGING_TIME_FORMAT = "%d-%m-%Y %H:%M:%S"


def _normalize_log_level(value: str, *, default: int) -> int:
    """Normalize user-provided log level strings to logging constants."""
    return getattr(logging, value.strip().upper(), default)


def setup_logging() -> None:
    """Set up logging for the demo application.

    Environment variables:
        LOG_LEVEL: Root logger level (default: WARNING)
        APP_LOG_LEVEL: Application logger level (default: INFO)
        LOG_FORMAT: Output format - 'json' or 'console' (default: console)
    """
    root_level = _normalize_log_level(os.environ.get("LOG_LEVEL", "WARNING"), default=logging.WARNING)
    app_level = _normalize_log_level(os.environ.get("APP_LOG_LEVEL", "INFO"), default=logging.INFO)
    log_format = os.environ.get("LOG_FORMAT", "console").strip().lower()

    if log_format == "json":
        # JSON format for production log aggregation
        fmt = '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}'
    else:
        # Human-readable console format
        fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    logging.basicConfig(level=root_level, format=fmt, datefmt=LOGGING_TIME_FORMAT, force=True)

    # Set application-specific log level
    for logger_name in ("insight_ui", "core"):
        logging.getLogger(logger_name).setLevel(app_level)
