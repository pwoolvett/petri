# coding=utf-8
"""Package documentation

.. versionadded:: 0.1.0
   Initial version.

"""
from petri import _logging_ as logging


class Metadata:
    def __init__(self):
        self.pyproject_ = None

    @property
    def pyproject(self):
        if not self.pyproject_:
            import toml
            import os

            dir_ = f"{os.path.dirname(os.path.abspath(__file__))}"
            fp = f"{dir_}/../pyproject.toml"
            self.pyproject_ = toml.load(fp)["tool"]["poetry"]

        return self.pyproject_

    def __getattr__(self, attr):
        val = self.pyproject.get(attr)
        if not val:
            raise AttributeError(f"package '{__package__}' has no attribute '{attr}'")
        return val

    __getitem__ = __getattr__


__meta__ = Metadata()


def __getattr__(attr_name: str) -> str:
    return __meta__[attr_name.replace("__", "")]


logger = logging.get_logger()
