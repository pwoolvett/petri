# -*- coding: utf-8 -*-
import pytest
from pathlib import Path

import toml


def read_pyproject_toml(pyproject_file):
    poetry = toml.load(pyproject_file)["tool"]["poetry"]
    dct = {k: v for k, v in poetry.items()}

    return {
        "name": dct["name"],
        "version": dct["version"],
        "summary": dct["description"],
        # "description": open(dct["readme"]).read(),
        "home_page": dct.get("home_page", "UNKNOWN"),
        "author": dct["authors"][0].split("<")[0].strip(),
        "author_email": dct["authors"][0]
        .split(" ")[-1]
        .strip()
        .replace("<", "")
        .replace(">", ""),
        "license": dct.get("license", "UNKNOWN"),
        # "platform": dct["dependencies"]['python'],
        # "requires_python": dct["dependencies"]["python"]
    }


@pytest.fixture
def expected():
    pyproject_file = Path(__file__).parent.parent.parent.joinpath(
        "pyproject.toml"
    )
    return read_pyproject_toml(pyproject_file)


@pytest.fixture
def script_file(tmpdir):
    root = tmpdir.mkdir("project_root")
    pyproject_file = root.join("pyproject.toml")
    script_file_ = root.join("test_script.py")
    pyproject_file.write(open("tests/unit/script_test/pyproject.toml").read())
    script_file_.write(open("tests/unit/script_test/script_example.py").read())

    return script_file_


@pytest.fixture
def project_init(tmpdir):
    root = tmpdir.mkdir("project_test")
    package = root.mkdir("a_package")

    pyproject_file = root.join("pyproject.toml")
    project_init_ = package.join("__init__.py")

    pyproject_file.write(open("tests/unit/project_test/pyproject.toml").read())
    project_init_.write(
        open("tests/unit/project_test/a_package/__init__.py").read()
    )

    return project_init_


def test_isolated_import():
    import petri  # pylint: disable=unused-import


@pytest.mark.parametrize(
    "name",
    [
        "name",
        "version",
        # "description",
        "summary",
        "home_page",
        "author",
        "author_email",
        "license",
        # "platform",
        # "requires_python",
    ],
)
def test_bootstrap(name, expected):
    import petri

    meta = petri.__meta__
    retreived = getattr(meta, name)
    assert retreived == expected[name]


def test_import_from_script(script_file):
    script = script_file.pyimport()
    assert script

    expected_ = toml.load(Path(script_file).parent.joinpath("pyproject.toml"))[
        "tool"
    ]["poetry"]

    meta = script.__meta__
    for name, xpected in expected_.items():
        try:
            retreived = getattr(meta, name)
        except BaseException:
            import pdb

            pdb.set_trace()
        assert xpected == retreived


def test_import_from_module(script_file):
    import importlib

    module = importlib.import_module(
        str(script_file).split("/")[-1].replace(".py", "")
    )
    assert module

    expected_ = toml.load(Path(script_file).parent.joinpath("pyproject.toml"))[
        "tool"
    ]["poetry"]

    meta = module.__meta__
    for name, xpected in expected_.items():
        try:
            retreived = getattr(meta, name)
        except BaseException:
            import pdb

            pdb.set_trace()
        assert xpected == retreived


def test_import_from_package(project_init):
    pkg = project_init.pyimport()
    assert pkg

    expected_ = read_pyproject_toml(
        Path(pkg.__meta__.main_file_str).parent.parent.joinpath(
            "pyproject.toml"
        )
    )
    meta = pkg.__meta__
    for name in ("name", "version"):
        assert getattr(meta, name) == expected_[name]
