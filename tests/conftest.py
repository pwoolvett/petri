import importlib
import sys
from pathlib import Path

import pytest
import toml


@pytest.yield_fixture(name="imported_petri")
def import_petri_fixture():
    if "petri" in globals():
        assert sys.getrefcount(a_pkg) == 3
        del petri

    if "petri" in sys.modules:
        del sys.modules["petri"]

    import petri

    importlib.reload(petri)
    return petri


@pytest.fixture(name="pyproject_toml")
def pyproject_toml_fixture():
    pyproject_file = Path(__file__).parent.parent / "pyproject.toml"
    poetry = toml.load(pyproject_file)["tool"]["poetry"]
    return {str(k): v for k, v in poetry.items()}
