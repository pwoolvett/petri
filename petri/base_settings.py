# -*- coding: utf-8 -*-
"""Settings  boilerplate."""

from abc import ABC
from os import environ
from pathlib import Path
from pprint import pformat
from typing import Optional
from typing import TypeVar
from typing import Type

from pydantic import ValidationError
from pydantic import BaseSettings as PydanticBaseSettings

from .logging_ import LogLevel, LogMode

Conf = TypeVar("Conf", bound="BaseSettings")
"""Generic variable that can be 'BaseSettings', or any subclass."""


class BaseSettings(PydanticBaseSettings, ABC):
    """Boilerplate for config loading and dotenv handling."""

    ENV: str
    """Mandatory class attribute."""

    APP: str
    """Name for the application importing petri."""

    BASEPATH: Path
    """Absolute path to the project directory"""

    PKG_PATH: Path
    """Absolute path to the package directory"""

    DATA: Path
    """Absolute path to the package directory"""

    LOG_LEVEL: LogLevel
    """Defines the logging level of the Application"""

    LOG_MODE: LogMode
    """Define allowed destinations for logs"""

    LOG_STORAGE: Path
    """Where to store the log files if `LOG_MODE` uses any"""

    class Config:  # pylint: disable=missing-docstring,too-few-public-methods
        env_prefix = ""

    @classmethod
    def read_env(cls, app_name: str = "") -> Optional[str]:
        """Allow custom `ENV` to be loaded depending on cls."""

        if app_name != "petri":
            return environ.get("ENV")

        return environ.get("PETRI_ENV", "development")

    @classmethod
    def descendants(cls):
        """Recursive subclasses."""

        children = cls.__subclasses__()
        for child in children.copy():
            children.extend(child.descendants())

        return children

    @classmethod
    def get_opts(cls, app_name: str = "") -> Optional[dict]:
        """Allow custom `ENV` to be loaded depending on cls."""

        if app_name != "petri":

            def bootstrap_filter(class_type):
                return class_type != _PetriSettings

        else:

            def bootstrap_filter(
                class_type
            ):  # pylint: disable=unused-argument
                return True

        descendants = {
            child.__fields__["ENV"].default: child
            for child in cls.descendants()
        }

        return {
            default_env: setting_class
            for default_env, setting_class in descendants.items()
            if default_env and bootstrap_filter(setting_class)
        }

    @staticmethod
    def build_kwargs(main_file: Path, app_name: str):
        """Define default values using the `__init__.py` file."""
        base_path = main_file.parent
        if main_file.stem == "__init__":
            package_path, base_path = base_path, base_path.parent

            if app_name != package_path.stem:
                msg = (
                    f"`app_name={app_name}` supplied, "
                    "but differs from`package_folder={package_path.stem}`"
                )
                raise ValueError(msg)

        else:
            package_path = base_path

        return {
            "APP": app_name,
            "BASEPATH": base_path,
            "PKG_PATH": package_path,
            "DATA": Path(base_path).joinpath("data"),
            "LOG_STORAGE": Path(base_path).joinpath("logs"),
        }

    @classmethod
    def from_env(
        cls: Type[Conf], main_file: Path, app_name: str, **cls_data
    ) -> Conf:
        """Allows instantiation from a single variable."""

        opts = cls.get_opts(app_name)

        if not opts:
            msg = f"No {cls} subclasses found"
            msg += f". Create one equipped with a default `ENV` (test/dev,etc)"
            raise ResourceWarning(msg)

        try:
            env = cls.read_env(app_name) or cls_data["env"]
        except KeyError as err:
            msg = "no `ENV` supplied"
            msg += f". Options: `{list(opts.keys())}`"
            raise KeyError(msg) from err

        try:
            config_cls: Type[Conf] = opts[env]
        except KeyError as err:
            msg = "invalid `ENV` supplied"
            msg += f". Received: `{env}`"
            msg += f". Options: `{list(opts.keys())}`"
            raise KeyError(msg) from err

        try:
            project_settings = cls.build_kwargs(main_file, app_name)
            config = config_cls(**project_settings, **cls_data)
            Path(config.DATA).mkdir(exist_ok=True, parents=True)
            Path(config.LOG_STORAGE).mkdir(exist_ok=True, parents=True)
        except ValidationError as err:
            print(err.json())
            raise err

        return config

    def to_str(self, dict_kw=None, **dumps_kw) -> str:
        """Formats the dictionary version as a string.

        Args:
            dict_kw ([dict], optional): kwargs for `BaseModel.dict`.
                Defaults to `{}`}.
            dumps_kw : optional kwargs forwarded to `pprint.pformat`.

        Returns:
            str: The formatted string version of the class as a
                dictionary.

        """

        dict_kw = dict_kw or {}

        return pformat(self.dict(**dict_kw), **dumps_kw)


class _PetriSettings(BaseSettings):
    """DO NOT USE THIS - Used only to bootstrap petri from within."""

    def __init__(self, *args, **kwargs):
        super(_PetriSettings, self).__init__(*args, **kwargs)
        if self.APP != "petri":  # pylint: disable=no-member
            raise ValueError("Only `petri` should use this class")

    class Config:  # pylint: disable=missing-docstring,too-few-public-methods
        env_prefix = "PETRI_"

    ENV = "development"
    LOG_LEVEL = LogLevel.ERROR
    LOG_MODE = LogMode.CONSOLE
