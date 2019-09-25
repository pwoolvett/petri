import logging
from datetime import datetime
from enum import IntEnum
from enum import IntFlag
from pathlib import Path
from typing import Callable

import autologging
import logstash
from pydantic import BaseSettings
import structlog
# import tzlocal


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

    FILE = 2
    """Log `autologging.TRACE` or more severe to trace file"""

    LOGSTASH = 4
    """Log `logging.ERROR` or more severe to an error file"""


class LogConfig(BaseSettings):
    LOG_MODE: LogMode
    LOG_LEVEL: LogLevel


def configure_logging(name, mode: LogMode):

    requires_console = mode & LogMode.CONSOLE
    requires_files = mode & LogMode.FILE
    requires_logstash = mode & LogMode.LOGSTASH

    # based on https://github.com/yeraydiazdiaz/structlog-elk/blob/master/app/log_config.py
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            # required as LogstashHandler uses `extra` for logging JSON values
            structlog.stdlib.render_to_log_kwargs,
        ],
        # required to mimic Flask's threadlocal context allowing
        # logging during the whole request process
        # context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.dev.ConsoleRenderer()
        )
    )

    app_logger = logging.getLogger(name)
    app_logger.addHandler(stream_handler)

    # for TCP use TCPLogstashHandler and port 5000
    logstash_handler = logstash.TCPLogstashHandler("logstash", 5000, version=1)
    app_logger.addHandler(logstash_handler)

    app_logger.setLevel(logging.INFO)
