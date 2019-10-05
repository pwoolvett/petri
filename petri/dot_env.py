# coding=utf-8
"""`.env` file handling ."""

import os
from pathlib import Path
from typing import Optional

from dotenv import find_dotenv
from dotenv import load_dotenv


def init_dotenv() -> Optional[str]:
    """Loc n' load dotenv file.

    Sets the location for a dotenv file containig envvars loads its
    contents.

    Raises:
        FileNotFoundError: When the selected location does not
        correspond to a file.

    Returns:
        Location of the dotenv file.

    """

    requested = os.environ.get("env_file")

    if requested:
        dotenv_path = Path(requested)
    else:
        candidate = find_dotenv(usecwd=True)
        if not candidate:
            return None
        dotenv_path = Path(candidate)

    if not (dotenv_path.exists() and dotenv_path.is_file()):
        raise IOError(f"Can't load {dotenv_path}")

    dotenv_str = str(dotenv_path)
    load_dotenv(dotenv_str)

    return dotenv_str
