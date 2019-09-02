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

from .metadata import Metadata
from .dotenv_ import init_dotenv
from .logging_ import create_logger, LogLevel, LogMode, make_tqdm
from .base_settings import BaseSettings


# pylint: disable=missing-docstring


def _initialize(**kwargs):
    """Instantiates all objects using a single python file."""

    main_file = kwargs["main_file"]
    pyproject_file = kwargs.get("pyproject_file")
    app_name = kwargs.get("app_name")

    metadata_ = Metadata(main_file, pyproject_file=pyproject_file)

    dle_path = Path(
        os.environ.get(
            "DOTENV_LOCATION", Path(os.getcwd()).resolve().joinpath(".env")
        )
    )

    dotenv_location_ = init_dotenv(path=dle_path, main_file=main_file)

    app_name = app_name or metadata_.package_name
    settings_ = BaseSettings.from_env(main_file, app_name)
    logger_ = create_logger(
        settings_.LOG_LEVEL, settings_.LOG_MODE, settings_.LOG_STORAGE
    )

    tqdm_ = make_tqdm(settings_.ENV)

    return metadata_, dotenv_location_, settings_, logger_, tqdm_


def initialize(main_file_str: str, app_name: str = "", **kw):

    main_file = Path(main_file_str)
    stem = main_file.stem

    init_kw = {"main_file": main_file, "app_name": app_name, **kw}

    if stem != "__init__":
        init_kw["pyproject_file"] = main_file.parent.joinpath("pyproject.toml")

    return _initialize(**init_kw)


# pylint: disable=invalid-name
__meta__, DOTENV_LOCATION, SETTINGS, logger, _ = initialize(__file__, "petri")
