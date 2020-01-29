# -*- coding: utf-8 -*-
"""Petri: 12-factor boilerplate in your python code."""

from pathlib import Path
from typing import Optional

from petri.dot_env import init_dotenv
from petri.loggin import configure_logging
from petri.metadata import Metadata
from petri.settings import BaseSettings

__version__ = "0.24.1"


class Petri:  # pylint: disable=R0903
    """Init & instantiate other modules & classes."""

    def __init__(
        self,
        init_dot_py: str,
        *,
        default_config: Optional[str] = None,
        force_log_control=False,
    ):
        self.__init_dot_py = init_dot_py
        self.__package = str(Path(init_dot_py).parent.stem)
        self.__default_config = default_config

        self.env_file: Optional[str] = init_dotenv()
        self.meta = Metadata(self.__package)
        self.settings = BaseSettings.from_envvar(
            self.__package,
            init_dot_py=self.__init_dot_py,
            default_config=self.__default_config,
        )
        self.log = configure_logging(
            self.__package,
            log_settings={
                "level": self.settings.LOG_LEVEL,
                "dest": self.settings.LOG_DEST,
                "formatter": self.settings.LOG_FORMAT,
                "log_file": self.settings.LOG_STORAGE,
            },
            force=force_log_control,
        )

        self.log.debug(
            "Package Initialization",
            **{
                "PETRI.package": self.__package,
                "PETRI.log_level": self.settings.LOG_LEVEL.value,
                "PETRI.log_dest": self.settings.LOG_DEST.value,
                "PETRI.log_fmt": self.settings.LOG_FORMAT.value,
                "PETRI.log_storage": str(self.settings.LOG_STORAGE),
                "PETRI.env_file": self.env_file,
            },
        )


pkg = Petri(__file__, default_config="petri.settings:_PetriSettings")
