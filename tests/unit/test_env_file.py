import importlib
import itertools
import os
import sys
from contextlib import nullcontext
from pathlib import Path

import pytest


from tests.unit import a_pkg_import
from tests.unit import temp_file

PWD_LOCATION = str(Path(os.getcwd()).joinpath(".env"))
CUSTOM_LOCATION = "sadfsdasdf.env"

env_file_opts = (None, PWD_LOCATION, CUSTOM_LOCATION)


@pytest.mark.parametrize(
    "requested,real", itertools.product(env_file_opts, env_file_opts)
)
def test_dotenv(monkeypatch, a_pkg_import, requested, real):

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
                with pytest.raises(IOError) as e_info:
                    a_pkg = a_pkg_import()
                # assert a_pkg.settings.FILE_LOCATED_AT = real # FIXME test for loader
        else:  # not requested
            if real == PWD_LOCATION:
                # from examples.a_pkg import a_pkg
                a_pkg = a_pkg_import()
                assert str(a_pkg.pkg.env_file) == real
                # assert a_pkg.settings.FILE_LOCATED_AT = real # FIXME test for loader
            else:
                # from examples.a_pkg import a_pkg
                a_pkg = a_pkg_import()
                assert a_pkg.pkg.env_file is None
