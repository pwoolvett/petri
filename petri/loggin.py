# -*- coding: utf-8 -*-
"""Configure a single logger."""

import logging.config
import uuid
from enum import Enum
from enum import IntEnum
from functools import wraps
from pathlib import Path

import structlog


class LogLevel(IntEnum):
    """Explicitly define allowed logging levels."""

    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    TRACE = 1 + logging.NOTSET
    NOTSET = logging.NOTSET


class LogDest(Enum):
    """Define allowed destinations for logs."""

    CONSOLE = "CONSOLE"
    """Log to console"""

    FILE = "FILE"
    """Log to file"""


class LogFormatter(Enum):
    """Define allowed destinations for logs."""

    JSON = "JSON"
    """JSONs, eg for filebeat or similar, for machines"""

    COLOR = "COLOR"
    """pprinted, colored, for humans"""


# def common_chain():
#     timestamper = structlog.processors.TimeStamper(fmt="iso")
#     return [
#         structlog.stdlib.add_logger_name,
#         structlog.stdlib.add_log_level,
#         structlog.stdlib.PositionalArgumentsFormatter(),
#         timestamper,
#         structlog.processors.StackInfoRenderer(),
#         structlog.processors.format_exc_info,
#     ]


COMMON_CHAIN = [
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
]


def configure_logging(
    name,
    level: LogLevel,
    dest: LogDest,
    formatter: LogFormatter,
    log_file: Path,
):
    """Setup logging with (hopefully) sane defaults.

    Args:
        name: Name for the logger.
        level: Level from where to start logging.
        dest: Whether to log to file or console.
        formatter: Whether to output data as json or colored, parsed
            logs.
        log_file: Where to store logfiles. Only used if ``dest='FILE'``.

    Returns:
        The configured logger.

    """

    if formatter == LogFormatter.JSON:
        fmt = {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": COMMON_CHAIN,
        }
    elif formatter == LogFormatter.COLOR:
        fmt = {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(
                colors=dest == LogDest.CONSOLE
            ),
            "foreign_pre_chain": COMMON_CHAIN,
        }
    else:
        raise NotImplementedError(  # pragma: no cover
            "Pydantic shouldn't allow this."
        )

    if dest == LogDest.CONSOLE:
        hndler = {
            "level": level,
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    elif dest == LogDest.FILE:
        hndler = {
            "level": level,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(log_file),
            "formatter": "default",
            "maxBytes": 10e6,
            "backupCount": 100,
        }
        log_file.parent.mkdir(parents=True, exist_ok=True)
    else:
        raise NotImplementedError(  # pragma: no cover
            "Pydantic shouldn't allow this."
        )

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"default": fmt},
            "handlers": {"default": hndler},
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": level.value,
                    "propagate": True,
                }
            },
        }
    )
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            *COMMON_CHAIN,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logger = structlog.get_logger(name)

    logger.trace = trace_using(logger)
    return logger


def trace_using(logger):
    """Decorator factory to trace callables.

    Args:
        logger: The logger to use for tracing

    Returns:
        The decorator, which takes a function and decorates it.

    """

    def real_decorator(func):
        """Decorate a callable to report args, kwargs and return."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            uuid_ = str(uuid.uuid4())
            qual = func.__qualname__
            args_repr = ",".join(repr(a) for a in args)
            kwargs_repr = ",".join(
                k + "=" + repr(v) for k, v in kwargs.items()
            )
            repr_ = f"{qual}({args_repr},{kwargs_repr})"
            with structlog.threadlocal.tmp_bind(
                logger,
                repr=repr_,
                uuid=uuid_,
                func=qual,
                args=args,
                kwargs=kwargs,
            ) as tmp_log:

                tmp_log.info(event="CALLED")
                retval = func(*args, **kwargs)
                tmp_log.info(event="RETURN", value=retval)
            return retval

        return wrapper

    return real_decorator
