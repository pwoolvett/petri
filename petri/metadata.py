# -*- coding: utf-8 -*-
"""Meta-info for the project, as read from`pyproject.toml`"""

import logging

from pathlib import Path
import toml

from importlib_metadata import distribution
from importlib_metadata import PackageNotFoundError


class Metadata:
    """Lazy-loader for project metadata."""

    def __init__(self, package: str, main_file_str: str):
        self.package = package
        self.main_file_str = main_file_str
        self.loaded = False

    def read_package_meta(self):
        meta = distribution(self.package).metadata
        return {k.lower().replace("-", "_"): v for k, v in meta.items()}

    def read_pyproject_meta(self):
        folder = Path(self.main_file_str).parent
        if "__init__" in self.main_file_str:
            folder = folder.parent

        pyproject_file = folder.joinpath("pyproject.toml")
        tool = toml.load(pyproject_file)["tool"]
        return {
            k: v
            for k, v in tool["poetry"].items()
        }

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError as att_err:
            if not self.loaded:
                self.loaded = True
                try:
                    meta = self.read_package_meta()
                except PackageNotFoundError:
                    meta = self.read_pyproject_meta()

                self.__dict__.update(
                    {k.lower().replace("-", "_"): v for k, v in meta.items()}
                )
            if name not in self.__dict__:
                msg = f"{name} not in {self.package}"
                raise AttributeError(msg) from att_err

            return self.__getattribute__(name)
