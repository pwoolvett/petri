# coding=utf-8
"""Handle project/application config from pyproject.toml.

Features include::

    * lazy-loading of project metadata from pyproject.toml
    * pre-loading a dotenv file
    * equipping a package/app/script/module with a pre-configured logger


.. versionadded:: 0.1.0
   Initial version.

"""
import os
from pathlib import Path

from .base_settings import BaseSettings
from .dotenv_ import init_dotenv
from .logging_ import LogLevel
from .logging_ import LogMode
from .logging_ import create_logger
from .logging_ import make_tqdm
from .metadata import Metadata


def initialize(main_file_str: str, app_name: str, **kw):
    """Instantiates all objects using a single python file."""

    main_file = Path(main_file_str)

    metadata_ = Metadata(app_name, main_file_str)

    dotenv_location_ = init_dotenv()

    settings_ = BaseSettings.from_env(main_file, app_name)

    logger_ = create_logger(
        app_name,
        settings_.LOG_LEVEL,
        settings_.LOG_MODE,
        settings_.LOG_STORAGE,
    )

    tqdm_ = make_tqdm(settings_.ENV)

    return metadata_, dotenv_location_, settings_, logger_, tqdm_


# pylint: disable=invalid-name
__meta__, DOTENV_LOCATION, SETTINGS, logger, _ = initialize(__file__, "petri")
