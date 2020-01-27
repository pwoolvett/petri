# -*- coding: utf-8 -*-

import petri

def test_version(pyproject_toml):
    assert petri.__version__ == pyproject_toml["version"]

    expected = {"name": "petri", "version": petri.__version__}
    for name, value in expected.items():
        assert getattr(petri.pkg.meta, name) == value
