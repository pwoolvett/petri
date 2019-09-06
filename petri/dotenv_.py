# coding=utf-8
"""`.env` file handling ."""

import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from dotenv import find_dotenv
from pydantic import BaseSettings
from pydantic import validator


class Milieu(BaseSettings):
    """Locate, validate `.env` file."""

    DOTENV_LOCATION: Optional[Path] = None

    class Config:
        env_prefix = ""


def init_dotenv(**kwargs) -> Path:
    """Loc n' load dotenv file.

    Sets the location for a dotenv file containig envvars loads its
    contents.

    Raises:
        FileNotFoundError: When the selected location does not
        correspond to a file.

    Returns:
        Location of the dotenv file.

    """

    dotenv_path = Milieu(**kwargs).DOTENV_LOCATION or find_dotenv(usecwd=True)
    path = Path(dotenv_path)
    if not (path.exists() and path.is_file()):
        raise IOError("File not found")
    load_dotenv(path, verbose=True)

    return path
