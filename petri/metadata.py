# -*- coding: utf-8 -*-
"""Meta-info for the project, as read from`pyproject.toml`"""

import logging
from pathlib import Path

import toml
from importlib_metadata import PackageNotFoundError
from importlib_metadata import distribution


class Metadata:
    """Lazy-loader for project metadata."""

    def __init__(self, package: str):
        self.package = package
        self._data = None

    @property
    def data(self):
        if not self._data:
            meta = distribution(self.package).metadata
            self._data = {k.lower(): v for k, v in dict(meta).items()}
        return self._data

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError as att_err:
            return self.data[name]
