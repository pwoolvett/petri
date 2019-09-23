# -*- coding: utf-8 -*-
"""Settings  boilerplate, loosely based on flask's."""

import logging
from abc import ABC
from importlib import import_module
import os
from pathlib import Path
from pprint import pformat

from typing import Any
from typing import Dict
from typing import Optional
from typing import Type
from typing import TypeVar

from pydantic import BaseSettings as PydanticBaseSettings
from pydantic import ValidationError


Conf = TypeVar("Conf", bound="BaseSettings")
"""Generic variable that can be 'BaseSettings', or any subclass."""


class BaseSettings(PydanticBaseSettings, ABC):
    """Boilerplate for config loading and dotenv handling."""

    BASEPATH: Path
    """Absolute path to the project directory"""

    PKG_PATH: Path
    """Absolute path to the package directory"""

    DATA: Path
    """Absolute path to the package directory"""

    # LOG_LEVEL: LogLevel
    # """Defines the logging level of the Application"""

    # LOG_MODE: LogMode
    # """Define allowed destinations for logs"""

    LOG_STORAGE: Path
    """Where to store the log files if `LOG_MODE` uses any"""

    class Config:  # pylint: disable=missing-docstring,too-few-public-methods
        env_prefix = ""

    @classmethod
    def from_envvar(
        cls, name: str, init_dot_py: str, default_config: Optional[str] = None
    ) -> "BaseSettings":
        """Instantiate settings class.

        Args:
            name: Name of the environment variable which contains
            the name of the settings class. Its contents must be of the
            form ``package.module:class``.

        Returns:

        """

        try:
            value = os.environ[name]
        except KeyError as no_env:
            msg = f"Environment Variable {name} not found."
            if default_config is None:
                raise KeyError(msg) from no_env
            logging.info(msg)
            value = default_config

        try:
            module, setting_cls = value.split(":")
        except ValueError as no_colon:
            msg = f"The environment variable {name} contains {value}, "
            msg += f" which does not have the format `[package.]module:class`"
            raise ValueError(
                f"The environment variable {name} contains"
            ) from no_colon

        cls_obj = getattr(import_module(module), setting_cls)

        kwargs = cls._build_kwargs(init_dot_py)

        return cls_obj(**kwargs)

    @staticmethod
    def _build_kwargs(init_dot_py: str) -> Dict[str, Any]:
        """Define default values using the `__init__.py` file."""
        package_path = Path(init_dot_py).parent
        base_path = package_path.parent
        return {
            "BASEPATH": base_path,
            "PKG_PATH": package_path,
            "DATA": Path(base_path).joinpath("data"),
            "LOG_STORAGE": Path(base_path).joinpath("logs"),
        }

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

    def __str__(self):
        return self.to_str()


class _PetriSettings(BaseSettings):
    """DO NOT USE THIS - Used only to bootstrap petri from within."""

    class Config:  # pylint: disable=missing-docstring,too-few-public-methods
        env_prefix = "PETRI_"

    ENV = "production"
    # LOG_LEVEL = LogLevel.ERROR
    # LOG_MODE = LogMode.CONSOLE
