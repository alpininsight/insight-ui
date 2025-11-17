import logging

import structlog

LOG_LEVEL = "INFO"
LOGGING_TIME_FORMAT = "%d-%m-%Y %H:%M:%S"


def setup_structlog() -> None:
    """Set up logger."""
    log_level = LOG_LEVEL

    logging.basicConfig(level=log_level, format="%(message)s")

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
            # Renders the event dictionary as a colorized, human-readable string for console output.
            structlog.dev.ConsoleRenderer(),
        ],
        # Creates a bound logger that filters log entries based on the log level.
        wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
        # Use a plain dictionary for the event dictionary.
        context_class=dict,
        # Use a print-based logger factory that prints log entries to the console.
        logger_factory=structlog.PrintLoggerFactory(),
        # Disables caching of the first logger instance used. Useful for dynamic logger configurations.
        cache_logger_on_first_use=False,
    )
