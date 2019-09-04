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

assert __meta__.release == "pre-alpha"
assert __meta__.maintainer == "Maintainer Name <maintainer@mail.com>"
assert __meta__.copyright == "A copyright"
assert __meta__.url == "www.script_example.com"
assert __meta__.license == "A License"
assert __meta__.name == "script_example"
assert __meta__.version == "1.2.3"
assert __meta__.description == "A description"
assert __meta__.readme == "README.rst"

assert __meta__.authors == ["Author Name <author@mail.com>"]
