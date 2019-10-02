# -*- coding: utf-8 -*-
"""Meta-info for the project, read using `importlib_metadata`"""

from typing import Any
from typing import Dict
from typing import Optional

from importlib_metadata import distribution


class Metadata:
    """Lazy-loader for project metadata."""

    def __init__(self, package: str):
        self.package = package
        self._data: Optional[Dict[str, Any]] = None

    @property
    def data(self) -> Dict[str, Any]:
        """Actual data."""
        if not self._data:
            meta = distribution(self.package).metadata
            self._data = {k.lower(): v for k, v in dict(meta).items()}
        return self._data

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self.data[name]
