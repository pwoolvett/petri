import os
import importlib
from dotenv import load_dotenv

from petri import _logging_

logger = _logging_.get_logger()

PACKAGE_SETTINGS = None
"""Settings module to be monkeypatched with environs"""


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


def load_dotenv_(pkg,):
    dotenv_location = os.getenv(
        "DOTENV_LOCATION", os.path.join(os.path.dirname(pkg), ".env")
    )
    """Location of the environment variales file

    By default, a :code:`.env` file is expected in the project's root.
    """

    if not os.path.isfile(dotenv_location):
        logger.error(FileNotFoundError(dotenv_location))

    logger.info(f"Using .env for environment variables: {dotenv_location}")
    load_dotenv(dotenv_location)


def monkey_patch_settings(module, pkg):
    global PACKAGE_SETTINGS

    if not PACKAGE_SETTINGS:
        PACKAGE_SETTINGS = importlib.import_module(".settings", pkg)
        for attr_name, attr_value in os.environ.items():
            try:
                getattr(PACKAGE_SETTINGS, attr_name)
            except AttributeError:
                setattr(PACKAGE_SETTINGS, attr_name, attr_value)
    return PACKAGE_SETTINGS


def init_dotenv(fn, module, pkg):
    load_dotenv_(pkg)
    s = monkey_patch_settings(module, pkg)
    return s
