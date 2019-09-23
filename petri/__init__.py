from importlib import import_module
from pathlib import Path
from typing import Optional

from petri.dot_env import init_dotenv
from petri.metadata import Metadata
from petri.settings import BaseSettings

__version__ = "0.23.0"


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)

    # Disable requests logging
    logging.getLogger("requests").propagate = False


class Petri:
    @staticmethod
    def pkg_2_envvar(name: str) -> str:
        return name.replace("-", "_").upper() + "_CONFIG"

    def __init__(self, init_dot_py: str, default_config: Optional[str] = None):
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


pkg = Petri(__file__, default_config="petri.settings:_PetriSettings")
