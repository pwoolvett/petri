from petri.loggin import LogFormatter
from petri.loggin import LogLevel
from petri.settings import BaseSettings


class Settings(BaseSettings):
    class Config:  # pylint: disable=missing-docstring,too-few-public-methods
        env_prefix = "A_PKG_"


class Production(Settings):
    ENV = "production"
    LOG_LEVEL = LogLevel.TRACE
    LOG_FORMAT = LogFormatter.JSON


class Development(Settings):
    ENV = "development"
    LOG_LEVEL = LogLevel.WARNING
    LOG_FORMAT = LogFormatter.COLOR


class Testing(Settings):
    ENV = "testing"
