#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""All things log-related: configuration, logger creation, etc."""

import logging
from datetime import datetime
from enum import IntFlag
from enum import IntEnum
from typing import Callable
from pathlib import Path

import autologging
import logzero
import tzlocal


class LogLevel(IntEnum):
    """Explicitly define allowed logging levels."""

    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    TRACE = autologging.TRACE


class LogMode(IntFlag):
    """Define allowed destinations for logs."""

    CONSOLE = 1
    """Log to console"""

    TRACE_FILE = 2
    """Log `autologging.TRACE` or more severe to trace file"""

    ERROR_FILE = 4
    """Log `logging.ERROR` or more severe to an error file"""

    TRACE_DB = 8
    """Log `autologging.TRACE` to `Trace` table in db"""

    ERROR_DB = 16
    """Log logging.ERROR or more severe to `Error` table in db"""


class LoggerFormatter(logzero.LogFormatter):
    """Define common logs formatting."""

    _fmt = "".join(
        [
            "%(color)s",
            "[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]",
            "%(end_color)s %(message)s",
        ]
    )
    _datefmt = "%Y/%m/%d@%H:%M:%S"  # "%Y-%m-%dT%H:%M:%S%z"

    def __init__(self):
        super(LoggerFormatter, self).__init__(
            fmt=self._fmt, datefmt=self._datefmt
        )


class Console(LoggerFormatter):
    """Define common logs formatting."""

    _datefmt = "%H:%M:%S"


class File(LoggerFormatter):
    """Define file logs formatting, ISO 8601, timezone-aware."""

    _fmt = "".join(
        [
            "[%(levelname).1s %(asctime)s | ",
            "%(name)s>%(filename)s:%(funcName)s:%(lineno)d] ",
            "%(message)s",
        ]
    )

    _datefmt = "%Y-%m-%dT%H:%M:%S%z"

    def formatTime(self, record, datefmt=None):
        return datetime.fromtimestamp(
            record.created, tz=tzlocal.get_localzone()
        ).strftime(datefmt)


def _attach_file_handler(filename, _logger, file_formatter, level):
    rotating_filehandler = logging.handlers.RotatingFileHandler(
        filename=filename, maxBytes=1e6, backupCount=3
    )
    setattr(rotating_filehandler, logzero.LOGZERO_INTERNAL_LOGGER_ATTR, True)
    rotating_filehandler.setLevel(level)
    rotating_filehandler.setFormatter(file_formatter)
    _logger.addHandler(rotating_filehandler)


def create_logger(
    level: LogLevel, mode: LogMode, log_storage: Path
) -> logging.Logger:
    """Configures custom  logger to files/console/db.

    Args:
        level: The logging level for the logger.
        mode: Where to log. See `LogMode`.
        log_storage: Where to store logs.

    Returns:
        The configured logger object.

    """

    requires_console = mode & LogMode.CONSOLE
    requires_files = mode & (LogMode.TRACE_FILE | LogMode.ERROR_FILE)
    requires_db = mode & (LogMode.TRACE_DB | LogMode.ERROR_DB)

    if requires_db:  # pragma: no cover
        raise NotImplementedError("RDBMS-based logging not implemented")

    _logger = logzero.setup_logger(
        name=__package__,
        level=level,
        formatter=Console(),
        disableStderrLogger=not requires_console,
    )

    if requires_files:
        file_formatter = File()

        if mode & LogMode.TRACE_FILE:
            _attach_file_handler(
                log_storage.joinpath("trace.log"),
                _logger,
                file_formatter,
                autologging.TRACE,
            )

        if mode & LogMode.ERROR_FILE:
            _attach_file_handler(
                log_storage.joinpath("errors.log"),
                _logger,
                file_formatter,
                logging.ERROR,
            )

    return _logger


def make_tqdm(env: str) -> Callable:
    """tqdm instance should not do anything in production."""

    if env == "production":
        return lambda x: x

    try:
        import tqdm  # pylint: disable=import-outside-toplevel, import-error

        return tqdm.tqdm
    except ModuleNotFoundError:
        return lambda x: x
