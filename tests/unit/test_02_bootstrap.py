# -*- coding: utf-8 -*-
from pathlib import Path

import pytest
import toml


@pytest.fixture
def pyproject_toml():
    pyproject_file = Path(__file__).parent.parent.parent / "pyproject.toml"
    poetry = toml.load(pyproject_file)["tool"]["poetry"]
    return {str(k): v for k, v in poetry.items()}


def test_version(pyproject_toml):  # pylint: disable=W0621
    import petri  # pylint: disable=C0415

    assert petri.__version__ == pyproject_toml["version"]

    expected = {"name": "petri", "version": petri.__version__}
    for name, value in expected.items():
        assert getattr(petri.pkg.meta, name) == value
