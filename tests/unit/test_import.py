# -*- coding: utf-8 -*-
import pytest


def test_isolated_import():
    import petri  # pylint: disable=unused-import


@pytest.mark.parametrize(
    "name",
    [
        ("project_name"),
        ("name"),
        ("release"),
        ("version"),
        ("description"),
        ("authors"),
        ("maintainer"),
    ],
)
def test_bootstrap(name):
    import petri

    meta = petri.__meta__
    assert getattr(meta, name)


def test_import_from_script(tmpdir):
    root = tmpdir.mkdir("project_root")
    pyproject_file = root.join("pyproject.toml")
    script_file = root.join("test_script.py")
    pyproject_file.write(open("tests/unit/script_pyproject.toml").read())
    script_file.write(open("tests/unit/sample_script.py").read())

    script_file.pyimport()


@pytest.mark.skip
def test_module_import(tmpdir):
    raise NotImplementedError("Emulate python -m ...")


def test_import_from_package(tmpdir):
    root = tmpdir.mkdir("project_root")
    package = root.mkdir("a_package")
    pyproject_file = root.join("pyproject.toml")
    script_file = package.join("__init__.py")
    pyproject_file.write(
        open("tests/unit/script_pyproject.toml")
        .read()
        .replace("script_example", "a_package")
    )
    script_file.write(
        open("tests/unit/sample_script.py")
        .read()
        .replace("script_example", "a_package")
    )

    script_file.pyimport()
