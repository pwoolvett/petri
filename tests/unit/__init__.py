import importlib
import os
import shutil
import sys
from contextlib import AbstractContextManager
from contextlib import contextmanager
from pathlib import Path

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
                assert sys.getrefcount(a_pkg) == 3  # pylint: disable=E0602
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
                import a_pkg  # pylint: disable=C0415,E0401

                importlib.reload(a_pkg)
            return a_pkg

    return importer  # provide the fixture value generator


class nullcontext(AbstractContextManager):  # pylint: disable=invalid-name
    """Context manager that does no additional processing.

    Used as a stand-in for a normal context manager, when a particular
    block of code is only sometimes used with a normal context manager:

    cm = optional_cm if condition else nullcontext()
    with cm:
        # Perform operation, using optional_cm if condition is True
    """

    def __init__(self, enter_result=None):
        self.enter_result = enter_result

    def __enter__(self):
        return self.enter_result

    def __exit__(self, *excinfo):  # pylint: disable=W0221
        pass
