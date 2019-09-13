# -*- coding: utf-8 -*-
"""A package: sample minimal package using petri"""

from petri import BaseSettings, initialize, LogMode, LogLevel


class PackageSettings(BaseSettings):
    pass


class ProdSettings(PackageSettings):
    ENV = "production"
    LOG_LEVEL = LogLevel.TRACE
    LOG_MODE = LogMode.ERROR_FILE


class DevSettings(PackageSettings):
    ENV = "development"
    LOG_LEVEL = LogLevel.INFO
    LOG_MODE = LogMode.CONSOLE | LogMode.ERROR_FILE


class TestSettings(PackageSettings):
    ENV = "testing"
    LOG_LEVEL = LogLevel.ERROR
    LOG_MODE = LogMode.CONSOLE


__meta__, DOTENV_LOCATION, SETTINGS, LOGGER, _ = initialize(
    __file__, __package__, PackageSettings
)
