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
    pyproject_file.write(open("tests/data/script_test/pyproject.toml").read())
    script_file.write(open("tests/data/script_test/script_example.py").read())

    script_file.pyimport()


@pytest.mark.skip
def test_module_import(tmpdir):
    raise NotImplementedError("Emulate python -m ...")


def test_import_from_package(tmpdir):
    root = tmpdir.mkdir("project_test")
    package = root.mkdir("a_package")

    pyproject_file = root.join("pyproject.toml")
    script_file = package.join("__init__.py")

    pyproject_file.write(open("tests/data/project_test/pyproject.toml").read())
    script_file.write(
        open("tests/data/project_test/a_package/__init__.py").read()
    )

    script_file.pyimport()
