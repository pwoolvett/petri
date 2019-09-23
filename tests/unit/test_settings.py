import importlib
import itertools
import os
import sys
from contextlib import nullcontext
from pathlib import Path
import shutil

import pytest

from isort.settings import from_path
from tests.unit import a_pkg_import
from tests.unit import temp_file
from tests.unit import restore_file


ENV_PREFIX = "A_PKG_"
CONFIG_SELECTOR = "CONFIG"
A_PKG_ENV_PREFIX = f"{ENV_PREFIX}{CONFIG_SELECTOR}"

A_PKG_INIT = str(
    Path(__file__).parent.parent.parent / "examples/a_pkg/a_pkg/__init__.py"
)

CONFIG_OPTS = (
    None,
    "a_pkg.settings:Production",
    "a_pkg.settings:Development",
    "wrong.Format",
    "pkg_non:Existent",
)


@pytest.mark.parametrize("envalue", CONFIG_OPTS)
def test_load_settings(monkeypatch, a_pkg_import, envalue):

    with monkeypatch.context() as patcher:
        if envalue is None:
            patcher.delenv(A_PKG_ENV_PREFIX, raising=False)
            
            with pytest.raises(KeyError) as e_info:
                a_pkg = a_pkg_import(setenv=False)

            with restore_file(A_PKG_INIT):
                with open(A_PKG_INIT, "r") as init:
                    txt_in = init.read()
                txt_out = txt_in.replace(
                    "pkg = Petri(__file__)",
                    "pkg = Petri(__file__, default_config='a_pkg.settings:Development')",
                )
                os.remove(A_PKG_INIT)
                with open(A_PKG_INIT, "w") as init:
                    init.write(txt_out)

                a_pkg = a_pkg_import(setenv=False)
                cls = a_pkg.pkg.settings.__class__
                assert (cls.__module__, cls.__name__) == tuple(
                    "a_pkg.settings:Development".split(":")
                )
            
        else:
            patcher.setenv(A_PKG_ENV_PREFIX, envalue, prepend=False)

            if envalue == "a_pkg.settings:Production":
                a_pkg = a_pkg_import(setenv=False)
                assert a_pkg.pkg.settings.ENV == "production"
    
            elif envalue == "a_pkg.settings:Development":
                a_pkg = a_pkg_import(setenv=False)
                assert a_pkg.pkg.settings.ENV == "development"
    
            elif envalue == "pkg_non:Existent":
                with pytest.raises(ImportError) as e_info:
                    a_pkg = a_pkg_import(setenv=False)
    
            elif envalue == "wrong.Format":
                with pytest.raises(ValueError) as e_info:
                    a_pkg = a_pkg_import(setenv=False)
                    assert "does not have the format" in e_info
            else:
                raise NotImplementedError
