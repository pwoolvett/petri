# -*- coding: utf-8 -*-
"""Python etensions and utilities."""


def to_upper_underscore(name: str) -> str:
    """Transform package name into uppercase with underscores.

    Example:

        >>> pkg_2_uu('a-pkg')
        'A_PKG'

    """
    return name.replace("-", "_").upper() + "_"


def pkg_2_envvar(name: str) -> str:
    """Transform package name into config selector string.

    Example:

        >>> pkg_2_envvar('a-pkg')
        'A_PKG_CONFIG'

    "In the face of ambiguity, refuse the temptation to guess."

    """
    return to_upper_underscore(name) + "CONFIG"
