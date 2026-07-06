"""Structured logging configuration with structlog."""

import logging
import os

import structlog

LOGGING_TIME_FORMAT = "%d-%m-%Y %H:%M:%S"


def _normalize_log_level(value: str, *, default: int) -> int:
    """Normalize user-provided log level strings to logging constants."""
    return getattr(logging, value.strip().upper(), default)


def setup_structlog() -> None:
    """Set up logger."""
    root_level = _normalize_log_level(os.environ.get("LOG_LEVEL", "WARNING"), default=logging.WARNING)
    app_level = _normalize_log_level(os.environ.get("APP_LOG_LEVEL", "INFO"), default=logging.INFO)
    log_format = os.environ.get("LOG_FORMAT", "console").strip().lower()
    renderer = structlog.processors.JSONRenderer() if log_format == "json" else structlog.dev.ConsoleRenderer()

    logging.basicConfig(level=root_level, format="%(message)s", force=True)

    structlog.configure(
        processors=[
            # Merges context variables from contextvars into the event dictionary.
            structlog.contextvars.merge_contextvars,
            # Adds the log level to the event dictionary.
            structlog.processors.add_log_level,
            # Adds stack info to the event dictionary, useful for debugging.
            structlog.processors.StackInfoRenderer(),
            # Adds callsite parameters (file name, function name, and line number) to the event dictionary.
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }
            ),
            # Adds a timestamp to the event dictionary.
            structlog.processors.TimeStamper(fmt=LOGGING_TIME_FORMAT, utc=False),
            renderer,
        ],
        # Creates a bound logger that filters log entries based on the log level.
        wrapper_class=structlog.make_filtering_bound_logger(app_level),
        # Use a plain dictionary for the event dictionary.
        context_class=dict,
        # Use a print-based logger factory that prints log entries to the console.
        logger_factory=structlog.PrintLoggerFactory(),
        # Disables caching of the first logger instance used. Useful for dynamic logger configurations.
        cache_logger_on_first_use=False,
    )
