"""Settings

Set any and all project variables here.

If you have two version of the project running, they should differ only in
variables set in this file.

Optionally, secret stuff is located in the a .env file, to be loaded here.
"""

from dotenv import load_dotenv
import os


DOTENV_LOCATION = os.getenv("DOTENV_LOCATION", ".env")
"""Location of the environment variales file

By default, a :code:`.env` file is expected in the project's root.
"""
load_dotenv(DOTENV_LOCATION)


def __getattr__(env_var_name: str) -> str:
    """Allow acessing environment variables as attributes in this module.

    Args:
        env_var_name: Name of the variable to access

    Returns:
      The value of the env var, according to :param:`os.environ`, after calling
      :func:`load_dotenv`.

    Example::

      $ cat .env
        ENV=DEV
      $ python -c "from unspsc import settings ; print(settings.UNSPSC_SQL)"
        DEV

    Note: Variable is loaded from env only "If an attribute is not found on a module
    object through the normal lookup"

    See Also:
      https://www.python.org/dev/peps/pep-0562/
    """
    return os.environ[env_var_name]
