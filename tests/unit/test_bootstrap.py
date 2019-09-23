# -*- coding: utf-8 -*-
import pytest
from pathlib import Path

import toml


@pytest.fixture
def pyproject_toml():
    pyproject_file = Path(__file__).parent.parent.parent.joinpath(
        "pyproject.toml"
    )
    poetry = toml.load(pyproject_file)["tool"]["poetry"]
    return {k: v for k, v in poetry.items()}


def test_version(pyproject_toml):
    import petri

    assert petri.__version__ == pyproject_toml["version"]

    expected = {"name": "petri", "version": petri.__version__}
    for name, value in expected.items():
        assert getattr(petri.pkg.meta, name) == value
