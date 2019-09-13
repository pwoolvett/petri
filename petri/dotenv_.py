# coding=utf-8
"""`.env` file handling ."""

import logging
from pathlib import Path
from typing import Optional

from dotenv import find_dotenv
from dotenv import load_dotenv
from pydantic import BaseSettings


class Milieu(BaseSettings):
    """Locate, validate `.env` file."""

    DOTENV_LOCATION: Optional[Path] = None

    class Config:
        env_prefix = ""


def init_dotenv(raise_error_if_not_found=False, **kwargs) -> Optional[Path]:
    """Loc n' load dotenv file.

    Sets the location for a dotenv file containig envvars loads its
    contents.

    Raises:
        FileNotFoundError: When the selected location does not
        correspond to a file.

    Returns:
        Location of the dotenv file.

    """

    dotenv_path = Path(
        Milieu(**kwargs).DOTENV_LOCATION or find_dotenv(usecwd=True)
    )

    if dotenv_path.exists() and dotenv_path.is_file():
        load_dotenv(dotenv_path, verbose=True)
        return dotenv_path
    else:
        msg = "Dotenv file %s not found", dotenv_path
        if dotenv_path:
            raise IOError(msg)
        else:
            logging.info(msg)

        return None
