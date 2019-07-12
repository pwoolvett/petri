import os
import sys
import pytest
from pydantic import ValidationError


def setup_function():
    """Make sure petri has not been imported.

    Because tests are changing dotenv variables in runtime, the project
    could have already been imported.

    The library `pydantic` does not reload settings after inittalization
    (and it shouldn't!)
    """

    for module_dot in [*sys.modules.keys()]:
        if module_dot.startswith("petri"):
            del sys.modules[module_dot]


@pytest.mark.parametrize(
    "varname,varval,err_cls",
    [
        ("DOTENV_LOCATION", "ajsdhfkhjasdfkjhasdjkf.env", FileNotFoundError),
        ("ENV", "produktioon", KeyError),
        ("LOG_MODE", "1234", ValidationError),
    ],
)
def test_environment(monkeypatch, varname, varval, err_cls):

    with monkeypatch.context() as patcher, pytest.raises(err_cls):
        patcher.setitem(os.environ, varname, varval)
        import petri  # pylint: disable=unused-import
