# -*- coding: utf-8 -*-
"""A package: sample minimal package using petri"""

from petri import BaseSettings, initialize, LogMode, LogLevel


class Settings(BaseSettings):
    pass


class ProdSettings(Settings):
    IS_DEFAULT = True
    ENV = "production"
    LOG_LEVEL = LogLevel.TRACE
    LOG_MODE = LogMode.ERROR_FILE


class DevSettings(Settings):
    ENV = "development"
    LOG_LEVEL = LogLevel.INFO
    LOG_MODE = LogMode.CONSOLE | LogMode.ERROR_FILE


class TestSettings(Settings):
    ENV = "testing"
    LOG_LEVEL = LogLevel.ERROR
    LOG_MODE = LogMode.CONSOLE


__meta__, DOTENV_LOCATION, SETTINGS, LOGGER, _ = initialize(
    __file__, "a_package", settings_cls=Settings
)
