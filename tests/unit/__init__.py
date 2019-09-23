from contextlib import contextmanager
from contextlib import nullcontext
import importlib
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


@contextmanager
def temp_file(path, mode):
    file = open(path, mode)
    try:
        yield file
    finally:
        file.close()
        os.remove(path)


@contextmanager
def restore_file(path):
    bkp = path + ".bkp"
    shutil.copyfile(path, bkp)

    try:
        yield
    finally:
        os.remove(path)
        os.replace(bkp, path)



@pytest.fixture(scope="function", params=[True, False])
def a_pkg_import(monkeypatch, request):
    def importer(setenv=True):
        with monkeypatch.context() as patcher:
            if setenv:
                patcher.setenv(
                    "A_PKG_CONFIG", "a_pkg.settings:Testing", prepend=False
                )

            if "a_pkg" in globals():
                assert sys.getrefcount(a_pkg) == 3
                del a_pkg

            if "a_pkg" in sys.modules:
                del sys.modules["a_pkg"]

            ctx = monkeypatch.context() if request.param else nullcontext()

            with ctx as patcher:
                if patcher:
                    patcher.syspath_prepend(
                        str(
                            Path(__file__).parent.parent.parent.joinpath(
                                "examples", "a_pkg"
                            )
                        )
                    )
                import a_pkg

                importlib.reload(a_pkg)
            return a_pkg

    return importer  # provide the fixture value generator
