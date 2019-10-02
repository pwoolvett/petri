import itertools
import os
from pathlib import Path

import pytest

from tests.unit import a_pkg_import  # pylint: disable=W0611
from tests.unit import nullcontext
from tests.unit import temp_file

PWD_LOCATION = str(Path(os.getcwd()).joinpath(".env"))
CUSTOM_LOCATION = "sadfsdasdf.env"

ENV_FILE_OPTS = (None, PWD_LOCATION, CUSTOM_LOCATION)


@pytest.mark.parametrize(
    "requested,real", itertools.product(ENV_FILE_OPTS, ENV_FILE_OPTS)
)
def test_dotenv(
    monkeypatch, a_pkg_import, requested, real
):  # pylint: disable=W0621

    env_file_path = temp_file(real, "w+") if real else nullcontext()

    with env_file_path as real_file, monkeypatch.context() as patcher:

        if requested:
            patcher.setenv("env_file", requested)
        else:
            patcher.delenv("env_file", raising=False)

        if real:
            real_file.write("FILE_LOCATED_AT={}\n".format(real))
            real_file.seek(0)

        if requested:
            if real == requested:
                a_pkg = a_pkg_import()
                assert a_pkg.pkg.env_file == requested
            else:
                with pytest.raises(IOError):
                    a_pkg = a_pkg_import()
        else:  # not requested
            if real == PWD_LOCATION:
                # from examples.a_pkg import a_pkg
                a_pkg = a_pkg_import()
                assert str(a_pkg.pkg.env_file) == real
            else:
                a_pkg = a_pkg_import()
                assert a_pkg.pkg.env_file is None
