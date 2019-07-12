# coding=utf-8
"""`.env` file handling ."""

import logging
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings


class Milieu(BaseSettings):
    """Locate, validate `.env` file."""

    DOTENV_LOCATION: Optional[Path] = None
    main_file: Optional[Path] = None
    "Use this as kwarg to generate default .env location."

    class Config:  # pylint: disable=missing-docstring,too-few-public-methods
        env_prefix = ""

    # pylint: disable=invalid-name,missing-docstring
    @property
    def DEFAULT_DOTENV_LOCATION(self) -> Optional[Path]:
        if self.main_file:
            base = self.main_file.parent
            if self.main_file.stem == "__init__":
                base = base.parent

            return base.joinpath(".env")

        return None


def init_dotenv(path: Path = None, **kwargs) -> Optional[Path]:
    """Loc n' load dotenv file.

    Sets the location for a dotenv file containig envvars loads its
    contents.

    Args:
        path: `Path` to the location of the `.env` file, if exists and
            is loaded.

    Kwargs:
        main_file: Location of the projects `__init__.py` file.
            It is only used to generate a default location in case path
            is not supplied.

    Raises:
        FileNotFoundError: When the selected location does not
        correspond to a file.

    Returns:
        Location of the dotenv file.

    """

    if path:
        kwargs.setdefault("DOTENV_LOCATION", path)
    milieu = Milieu(**kwargs)
    dotenv_path = milieu.DOTENV_LOCATION

    if dotenv_path:
        if not (dotenv_path.exists() and dotenv_path.is_file()):
            raise FileNotFoundError(
                "`.env` file does not exist in {}".format(str(dotenv_path))
            )
    else:
        logging.info("`DOTENV_LOCATION` env not supplied")
        dotenv_path = milieu.DEFAULT_DOTENV_LOCATION
        if dotenv_path and dotenv_path.exists() and dotenv_path.is_file():
            logging.info("`DOTENV_LOCATION` defaulted to %s", dotenv_path)
        else:
            return None

    load_dotenv(dotenv_path)

    return dotenv_path
