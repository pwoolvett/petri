# -*- coding: utf-8 -*-
"""Settings  boilerplate, loosely based on flask's."""

import logging
import os
from abc import ABC
from importlib import import_module
from pathlib import Path
from pprint import pformat
from typing import Optional
from typing import TypeVar

from pydantic import BaseSettings as PydanticBaseSettings
from pydantic import validator

from petri.loggin import LogDest
from petri.loggin import LogFormatter
from petri.loggin import LogLevel

Conf = TypeVar("Conf", bound="BaseSettings")
"""Generic variable that can be 'BaseSettings', or any subclass."""

FORMAT_SEL = "[package.]module:class"


class BaseSettings(PydanticBaseSettings, ABC):
    """Boilerplate for config loading and dotenv handling."""

    INIT_DOT_PY: str = None  # type: ignore
    """Location of the ``package/__init__.py``."""

    BASEPATH: Path = None  # type: ignore
    """Absolute path to the project directory"""

    PKG_PATH: Path = None  # type: ignore
    """Absolute path to the package directory"""

    DATA: Path = None  # type: ignore
    """Absolute path to the package directory"""

    LOG_LEVEL: LogLevel = LogLevel.WARNING
    """Defines the logging level of the Application"""

    LOG_DEST: LogDest = LogDest.CONSOLE
    """Define allowed destinations for logs"""

    LOG_FMT: LogFormatter = LogFormatter.COLOR
    """Define allowed formats for logs."""

    LOG_STORAGE: Path = None  # type: ignore
    """Where to store the log file."""

    @validator("BASEPATH", pre=True, always=True)
    def validate_basepath(cls, v, values):  # pylint: disable=E0213,R0201
        """Dynamically defined as ``__init__.py``'s folder."""
        init_dot_py = values["INIT_DOT_PY"]
        return v or Path(init_dot_py).parent

    @validator("PKG_PATH", pre=True, always=True)
    def validate_pkg_path(cls, v, values):  # pylint: disable=E0213,R0201
        """Dynamically defined as ``__init__.py``'s folder's parent."""
        return v or values["BASEPATH"].parent

    @validator("DATA", pre=True, always=True)
    def validate_data(cls, v, values):  # pylint: disable=E0213,R0201
        """Dynamically defined as ``__init__.py``'s folder's sibling."""
        return v or Path(values["BASEPATH"]).joinpath("data")

    @validator("LOG_STORAGE", pre=True, always=True)
    def validate_log_storage(cls, v, values):  # pylint: disable=E0213,R0201
        """Dynamically defined in ``__init__.py``'s folder's sibling."""
        return v or Path(values["BASEPATH"]).joinpath("logs") / "logs.log"

    class Config:  # pylint: disable=missing-docstring,too-few-public-methods
        env_prefix = ""

    @classmethod
    def from_envvar(
        cls, name: str, init_dot_py: str, default_config: Optional[str] = None
    ) -> "BaseSettings":
        """Instantiate settings class.

        Args:
            name: Name of the environment variable which contains the
                name of the settings class. Its contents must be of the
                form ``package.module:class``.

        Raises:
            KeyError: The received envvar cant be found
            ValueError: A wrong format was used for the envvar

        Returns:
            The instantiated class.

        """

        try:
            value = os.environ[name]
        except KeyError as no_env:
            msg = f"Environment Variable `{name}` not found."
            if default_config is None:
                msg += " Either supply it indicating the class to load"
                msg += (
                    ", or instantiate `Petri` with a `default_config` kwarg."
                )
                msg += f" In any case, the format must be `{FORMAT_SEL}`."
                raise KeyError(msg) from no_env
            logging.info(msg)
            value = default_config

        try:
            module, setting_cls = value.split(":")
        except ValueError as wrong_fmt:
            msg = f"The environment variable {name} contains {value}, "
            msg += f" which does not have the format `{FORMAT_SEL}`"
            raise ValueError(msg) from wrong_fmt

        cls_obj = getattr(import_module(module), setting_cls)

        return cls_obj(INIT_DOT_PY=init_dot_py)

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

    LOG_LEVEL = LogLevel.WARNING
    LOG_DEST = LogDest.CONSOLE
    LOG_FMT = LogFormatter.COLOR
