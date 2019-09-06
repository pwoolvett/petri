# -*- coding: utf-8 -*-
"""sample python module using petri"""

from petri import BaseSettings, initialize, LogMode, LogLevel


class ProdSettings(BaseSettings):
    ENV = "production"
    LOG_LEVEL = 40
    LOG_MODE = LogMode.ERROR_FILE


class DevSettings(BaseSettings):
    ENV = "development"
    LOG_LEVEL = LogLevel.INFO
    LOG_MODE = LogMode.CONSOLE


class TestSettings(BaseSettings):
    ENV = "testing"
    LOG_LEVEL = LogLevel.ERROR
    LOG_MODE = LogMode.CONSOLE


__meta__, DOTENV_LOCATION, SETTINGS, LOGGER, _ = initialize(
    __file__, "script_example"
)
