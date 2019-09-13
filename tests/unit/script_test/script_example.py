# -*- coding: utf-8 -*-
"""sample python module using petri"""

from petri import BaseSettings, initialize, LogMode, LogLevel


class MySettings(BaseSettings):
    ENV = "testing"


class ProdSettings(MySettings):
    ENV = "production"
    LOG_LEVEL = 40
    LOG_MODE = LogMode.ERROR_FILE


class DevSettings(MySettings):
    ENV = "development"
    LOG_LEVEL = LogLevel.INFO
    LOG_MODE = LogMode.CONSOLE


class TestSettings(MySettings):
    ENV = "testing"
    LOG_LEVEL = LogLevel.ERROR
    LOG_MODE = LogMode.CONSOLE


__meta__, DOTENV_LOCATION, SETTINGS, LOGGER, _ = initialize(
    __file__, "script_example", settings_cls=MySettings
)
