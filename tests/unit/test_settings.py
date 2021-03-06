import inspect
import itertools
import os
from pathlib import Path

import pytest

from petri.loggin import LogFormatter
from petri.loggin import LogLevel
from petri.settings import BaseSettings
from tests.unit import a_pkg_import  # pylint: disable=W0611
from tests.unit import restore_file
from tests.unit import temp_file  # pylint: disable=W0611

ENV_PREFIX = "A_PKG_"
CONFIG_SELECTOR = "CONFIG"
A_PKG_ENV_PREFIX = f"{ENV_PREFIX}{CONFIG_SELECTOR}"

A_PKG_INIT = str(
    Path(__file__).parent.parent.parent
    / "tests/fixtures/a_pkg/a_pkg/__init__.py"
)

CONFIG_OPTS = (
    None,
    "a_pkg.settings:Production",
    "a_pkg.settings:Development",
    "wrong.Format",
    "pkg_non:Existent",
)


@pytest.mark.parametrize("envalue", CONFIG_OPTS)
def test_load_settings(
    monkeypatch, a_pkg_import, envalue
):  # pylint: disable=W0621

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
                    "pkg = Petri(__file__, default_config='a_pkg.settings:Development')",  # pylint: disable=C0301
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


def make_setting_obj(outer, inner, parent, additional_config, prefix):

    config = {}
    if prefix:
        config["env_prefix"] = "config_"

    if additional_config:
        config["case_sensitive"] = True

    if inner == "tuple":
        config = (config,)
    elif inner == "cls":
        config = type("Config", (), config)

    outer_obj = {
        "ENV": "Testing",
        "LOG_LEVEL": LogLevel.WARNING,
        "LOG_FORMAT": LogFormatter.COLOR,
        "Config": config,
    }

    if config:
        outer_obj["Config"] = config

    if outer == "tuple":
        outer_obj = (outer_obj,)
    elif inner == "cls":
        outer_obj = type(
            "Outer", (BaseSettings,) if parent else tuple(), outer_obj
        )

    return outer_obj


KIND_OPTS = ("cls", "dict", "tuple")
TF = (True, False)


@pytest.mark.parametrize(
    "outer,inner,parent,additional_config,prefix",
    itertools.product(KIND_OPTS, KIND_OPTS, TF, TF, TF),
)
def test_validate_class(outer, inner, parent, additional_config, prefix):
    config_obj = make_setting_obj(
        outer, inner, parent, additional_config, prefix
    )

    def validate():
        return BaseSettings.validate_class("pkg-name", "Outer", config_obj)

    if prefix or ("tuple" in (outer, inner)):
        with pytest.raises(ValueError):
            validate()
        return

    validated = validate()

    assert isinstance(validated, type)
    assert validated.__name__ == "Outer"
    assert hasattr(validated, "Config")
    assert BaseSettings in inspect.getmro(validated)
    assert hasattr(validated.Config, "env_prefix")
    assert validated.Config.env_prefix == "PKG_NAME_"
