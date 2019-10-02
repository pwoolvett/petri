from petri.settings import BaseSettings


class Settings(BaseSettings):
    class Config:  # pylint: disable=missing-docstring,too-few-public-methods
        env_prefix = "A_PKG_"


class Production(Settings):
    ENV = "production"


class Development(Settings):
    ENV = "development"


class Testing(Settings):
    ENV = "testing"
