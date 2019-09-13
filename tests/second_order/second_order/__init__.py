# -*- coding: utf-8 -*-
"""Second order: sample package using  a package which uses petri"""

from petri import BaseSettings, initialize, LogMode, LogLevel

import a_pkg
from a_pkg import my_module


class MyPackage(BaseSettings):
    pass


class ProdSettings(MyPackage):
    ENV = "production"
    LOG_LEVEL = LogLevel.TRACE
    LOG_MODE = LogMode.ERROR_FILE


class DevSettings(MyPackage):
    ENV = "development"
    LOG_LEVEL = LogLevel.INFO
    LOG_MODE = LogMode.CONSOLE | LogMode.ERROR_FILE


class TestSettings(MyPackage):
    ENV = "testing"
    LOG_LEVEL = LogLevel.ERROR
    LOG_MODE = LogMode.CONSOLE


__meta__, DOTENV_LOCATION, SETTINGS, LOGGER, _ = initialize(
    __file__, "second_order", settings_cls=MyPackage
)
