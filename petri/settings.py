# -*- coding: utf-8 -*-
"""Settings  boilerplate, loosely based on flask's."""

import inspect
import logging
import os
from abc import ABC
from importlib import import_module
from pathlib import Path
from pprint import pformat
from typing import Any
from typing import Dict
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from pydantic import BaseSettings as PydanticBaseSettings
from pydantic import validator

from petri.ext import pkg_2_envvar
from petri.ext import to_upper_underscore
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

    LOG_FORMAT: LogFormatter = LogFormatter.COLOR
    """Define allowed formats for logs."""

    LOG_STORAGE: Path = None  # type: ignore
    """Where to store the log file."""

    class Config:  # pylint: disable=C0115,R0903
        env_prefix = "DO_NOT_USE_THIS"

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

    @classmethod
    def from_envvar(
        cls,
        pkg_name: str,
        init_dot_py: str,
        default_config: Optional[str] = None,
    ) -> "BaseSettings":
        """Instantiate settings class.

        Args:
            pkg_name: Name of the package.

        Raises:
            KeyError: The received envvar can't be found.
            ValueError: A wrong format was used for the envvar.

        Returns:
            The instantiated class.

        """

        config_selector_envvar = pkg_2_envvar(pkg_name)

        try:
            value = os.environ[config_selector_envvar]
        except KeyError as no_env:
            msg = f"Environment Variable `{config_selector_envvar}` not found."
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
            module, cls_name = value.split(":")
        except ValueError as wrong_fmt:
            msg = "The environment variable {config_selector_envvar}"
            msg += f" contains {value},"
            msg += f" which does not have the format `{FORMAT_SEL}`"
            raise ValueError(msg) from wrong_fmt

        config_obj = getattr(import_module(module), cls_name)
        cls_obj = cls.validate_class(pkg_name, cls_name, config_obj)

        return cls_obj(INIT_DOT_PY=init_dot_py)

    @classmethod
    def _dict_2_cls(cls, config_obj, cls_name):
        if "Config" in config_obj:
            config = config_obj.pop("Config")
            if isinstance(config, dict):
                config_obj["Config"] = type("Config", (), config)
            elif not isinstance(config, type):
                msg = f"The `Config` attribute in `{cls_name}`"
                msg += " must either be a class or a dict"
                msg += f". Received: {type(config)}"
                raise ValueError(msg) from None

        return type(cls_name, (BaseSettings,), config_obj)

    @classmethod
    def _impose_basesettings_parent(cls, config_obj, cls_name, env_prefix):
        if hasattr(config_obj, "Config"):
            defined_prefix = (
                hasattr(
                    config_obj.Config, "env_prefix"  # type: ignore
                )
                and config_obj.Config.env_prefix  # type: ignore
                != BaseSettings.Config.env_prefix  # type: ignore
            )
            if defined_prefix:
                msg = f"The `Config` attribute in {cls_name}"
                msg += " must not define `env_prefix`"
                msg += f". Petri will use {env_prefix}"
                msg += ". Received: {}".format(
                    config_obj.Config.env_prefix  # type: ignore
                )
                raise ValueError(msg) from None

        return type(cls_name, (BaseSettings, config_obj), {})

    @classmethod
    def validate_class(
        cls,
        pkg_name: str,
        cls_name: str,
        config_obj: Union[Dict[str, Any], type, Type["BaseSettings"]],
    ) -> Type["BaseSettings"]:
        """Make sure an object is a valid petri setting.

        Args:
            pkg_name: Name of the packege the settings belongs to. Used to
                define the ``env_prefix``.
                See https://pydantic-docs.helpmanual.io/usage/settings/.
            cls_name: Name of the settings class. Used to dynamically
                create classes which fullfill petri requirements.
            config_obj: Data container: the contents of the settings class.

        Raises:
            NotImplementedError: [description]
            ValueError: Not supported datatype for ``config_obj``.
            ValueError: If ``config_obj`` defines ``Config.env_prefix``

        Returns:
            The validated class. It will
                (a) Inherit form `BaseSettings`,
                (b) Contain  ``Config`` with a petri-defined ``env_prefix``.

        """

        if isinstance(config_obj, dict):
            cls_obj = cls._dict_2_cls(config_obj, cls_name)
            return cls.validate_class(pkg_name, cls_name, cls_obj)

        env_prefix = to_upper_underscore(pkg_name)
        if isinstance(config_obj, type):
            if BaseSettings not in inspect.getmro(config_obj):
                cls_obj = cls._impose_basesettings_parent(
                    config_obj, cls_name, env_prefix
                )
                return cls.validate_class(pkg_name, cls_name, cls_obj)
        else:
            msg = f"The {cls_name} object"
            msg += " must either be a class or a dict"
            msg += f". Received: {type(config_obj)}"
            raise ValueError(msg) from None

        if not hasattr(config_obj, "Config"):  # pragma: no cover
            raise NotImplementedError("Could not define Config attribute")

        config_subcls = config_obj.Config  # type: ignore
        if not isinstance(config_subcls, type):
            if isinstance(config_subcls, dict):
                config_obj.Config = type(  # type: ignore
                    "Config", (), config_subcls
                )
            else:
                msg = f"The `Config` attribute in {cls_name}"
                msg += " must either be a class or a dict"
                msg += f". Received: {type(config_subcls)}"
                raise ValueError(msg) from None

        defined_prefix = (
            hasattr(config_obj.Config, "env_prefix")  # type: ignore
            and config_obj.Config.env_prefix  # type: ignore
            != BaseSettings.Config.env_prefix  # type: ignore
        )
        if defined_prefix:
            msg = f"The `Config` attribute in {cls_name}"
            msg += " must not define `env_prefix`"
            msg += f". Petri will use {env_prefix}"
            msg += (
                f". Received: {config_obj.Config.env_prefix}"  # type: ignore
            )
            raise ValueError(msg) from None

        config_obj.Config.env_prefix = env_prefix  # type: ignore
        return config_obj

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


class ProductionLog:  # pylint: disable=R0903
    """Log [EVERYTHING] as [JSON] to [CONSOLE]."""

    LOG_LEVEL = LogLevel.TRACE
    LOG_DEST = LogDest.CONSOLE
    LOG_FORMAT = LogFormatter.JSON


class DevelopmentLog:  # pylint: disable=R0903
    """Log [WARNING] (or more severe) as [COLORED TXT] to [CONSOLE]."""

    LOG_LEVEL = LogLevel.WARNING
    LOG_DEST = LogDest.CONSOLE
    LOG_FORMAT = LogFormatter.COLOR


class _PetriSettings(BaseSettings, DevelopmentLog):
    """DO NOT USE THIS - Used only to bootstrap petri from within."""
