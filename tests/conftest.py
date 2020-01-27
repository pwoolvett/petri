from pathlib import Path

import pytest
import toml

@pytest.fixture(name='pyproject_toml')
def pyproject_toml_fixture():
    import petri
    pyproject_file = Path(__file__).parent.parent / "pyproject.toml"
    poetry = toml.load(pyproject_file)["tool"]["poetry"]
    return {str(k): v for k, v in poetry.items()}
