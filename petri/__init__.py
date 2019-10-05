# -*- coding: utf-8 -*-
"""Petri: 12-factor boilerplate in your python code."""

from importlib import import_module
from pathlib import Path
from typing import Optional

from petri.dot_env import init_dotenv
from petri.loggin import configure_logging
from petri.metadata import Metadata
from petri.settings import BaseSettings

__version__ = "0.23.1"


class Petri:  # pylint: disable=R0903
    """Init & instantiate other modules & classes."""

    @staticmethod
    def pkg_2_envvar(name: str) -> str:
        """Transform package name into config selector string.

        Example:

            >>> pkg_2_envvar('a-pkg')
            'A_PKG_CONFIG'

        """
        return name.replace("-", "_").upper() + "_CONFIG"

    def __init__(
        self, init_dot_py: str, *, default_config: Optional[str] = None
    ):
        self.__init_dot_py = init_dot_py
        self.__package = str(Path(init_dot_py).parent.stem)
        self.__default_config = default_config

        self.env_file: Optional[str] = init_dotenv()
        self.meta = Metadata(self.__package)
        self.settings = BaseSettings.from_envvar(
            self.pkg_2_envvar(self.__package),
            init_dot_py=self.__init_dot_py,
            default_config=self.__default_config,
        )
        self.log = configure_logging(
            self.__package,
            self.settings.LOG_LEVEL,
            self.settings.LOG_DEST,
            self.settings.LOG_FMT,
            self.settings.LOG_STORAGE,
        )

        self.log.info(str(self.__dict__))


pkg = Petri(__file__, default_config="petri.settings:_PetriSettings")
