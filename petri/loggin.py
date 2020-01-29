# -*- coding: utf-8 -*-
"""Configure a single logger."""

import logging.config
import uuid
from enum import Enum
from enum import IntEnum
from functools import wraps
from pathlib import Path
from typing import Any
from typing import Dict

import structlog

try:  # pragma: no cover
    import colorama  # pylint: disable=W0611,

    COLORAMA_INSTALLED = True
except ImportError:
    COLORAMA_INSTALLED = False

try:  # pragma: no cover
    import tqdm  # pylint: disable=W0611,

    TQDM_INSTALLED = True
except ImportError:
    TQDM_INSTALLED = False


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


COMMON_CHAIN = [
    structlog.threadlocal.merge_threadlocal_context,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
]


def maybe_patch_tqdm(logger, dev_mode):
    """Replaces ``tqdm.tqdm`` calls with noops."""

    if (not dev_mode) and TQDM_INSTALLED:

        def _tqdm(*a, **kw):
            """Does nothing.

            Kills tqdm

            """
            logger.warning("tqdm usage supressed", args=a, kwargs=kw)
            return a[0]

        tqdm.tqdm = _tqdm


def _build_formatter(formatter, dev_mode):
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
                colors=dev_mode and COLORAMA_INSTALLED
            ),
            "foreign_pre_chain": COMMON_CHAIN,
        }
    else:
        raise NotImplementedError(  # pragma: no cover
            "Pydantic shouldn't allow this."
        )
    return fmt


def _build_hndler(dest, level, log_file: Path):
    common_kw = {
        "level": level,
        "formatter": "default",
    }
    if dest == LogDest.CONSOLE:
        return {"class": "logging.StreamHandler", **common_kw}

    if dest == LogDest.FILE:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        return {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(log_file),
            "maxBytes": 10e6,
            "backupCount": 100,
            **common_kw,
        }

    raise NotImplementedError(  # pragma: no cover
        "Pydantic shouldn't allow this."
    )


def _config_native_logging(fmt, hndler, level):
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


def _config_structlog():
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


def _control_logging(
    fmt, hndler, level, greedy: bool,
):

    if greedy:
        structlog.reset_defaults()

    already_configured = structlog.is_configured()
    if already_configured:
        pass

    if greedy or not already_configured:
        _config_native_logging(fmt, hndler, level)

    _config_structlog()


def configure_logging(
    name, log_settings: Dict[str, Any], force=False,
):
    """Setup logging with (hopefully) sane defaults.

    Args:
        name: Name for the logger.
        log_settings: configuration for the logger. It must contain the
            following items:
            * level: Level from where to start logging.
            * dest: Whether to log to file or console.
            * formatter: Whether to output data as json or colored, parsed
                logs.
            * log_file: Where to store logfiles. Only used if ``dest='FILE'``.
        force: Whether to configure the loggers or just
            instantiate one.

    Returns:
        The configured logger.

    """

    level: LogLevel = log_settings["level"]
    dest: LogDest = log_settings["dest"]
    formatter: LogFormatter = log_settings["formatter"]
    log_file: Path = Path(log_settings["log_file"]).resolve()
    dev_mode = (formatter == LogFormatter.COLOR) and (dest == LogDest.CONSOLE)

    fmt = _build_formatter(formatter, dev_mode)
    hndler = _build_hndler(dest, level, log_file)

    _control_logging(fmt, hndler, level, force)

    logger = structlog.get_logger(name)
    logger.trace = trace_using(logger)
    maybe_patch_tqdm(logger, dev_mode)
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
