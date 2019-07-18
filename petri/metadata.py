# -*- coding: utf-8 -*-
"""Meta-info for the project, as read from`pyproject.toml`"""

from pathlib import Path
from typing import Optional, List

import toml

from pydantic.types import EmailStr, UrlStr


class SemVer:  # pylint: disable=too-few-public-methods
    """Semantic versioned string."""

    def __init__(self, *, string: str = "", **kwargs):
        if string and len(string.split(".")) == 3:
            self.string = string
            self._major, self._minor, self._patch = string.split(".")
        elif all(x in kwargs for x in ("major", "minor", "patch")):
            self._major = kwargs["major"]
            self._minor = kwargs["minor"]
            self._patch = kwargs["patch"]
            self.string = ".".join((self._major, self._minor, self._patch))
        else:
            raise ValueError("Correct SemVer format is `major.minor.patch`")

    def __repr__(self):
        return self.string

    __str__ = __repr__


class Person:  # pylint: disable=too-few-public-methods
    """Name + email."""

    def __init__(
        self,
        name: str,
        *,
        surname: str = "",
        email: Optional[EmailStr] = None,  # type: ignore
    ):
        self.name = name
        self.surname = surname
        self.email = email
        self._str = ""

    @property
    def _as_str(self) -> str:
        if not self._str:
            txt = self.name + self.surname
            if self.email:
                txt += f"<{self.email}>"
            self._str = txt
        return self._str

    def __repr__(self):
        return self._as_str

    __str__ = __repr__


class Metadata:  # pylint: disable=too-few-public-methods,
    """Lazy-loader for pyproject `[tool.poetry]` and `[tool.meta]`.

    Examples:

        $ ls
        __init__.py  pyproject.toml  module.py

        $ cat __init__.py
        from petri import Metadata
        M = Metadata(__file__)

        >>> from project import M
        >>> M.authors

    """

    name: str
    release: str
    maintainer: Person
    copyright: str
    url: UrlStr
    version: SemVer
    description: str
    readme: str
    authors: List[Person]

    @property
    def project_name(self) -> str:  # pylint: disable=missing-docstring
        return self.name

    @property
    def author(self) -> Person:  # pylint: disable=missing-docstring
        return self.authors[0]

    def __init__(self, main_file: Path, pyproject_file: Optional[Path] = None):
        self.pyproject_file = (
            pyproject_file
            or main_file.parent.parent.joinpath("pyproject.toml")
        )
        if not self.pyproject_file.exists():
            raise FileNotFoundError(self.pyproject_file)  # pragma: no cover

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            tool = toml.load(self.pyproject_file)["tool"]
            self.__dict__.update(
                {
                    k: v
                    for section in ("poetry", "meta")
                    for k, v in tool[section].items()
                }
            )

            if name not in self.__dict__:
                raise AttributeError(f"{name} not in {self.pyproject_file}")

            return self.__getattribute__(name)
