def test_import(imported_petri):
    assert imported_petri


def test_bootstrap(imported_petri, pyproject_toml):
    petri = imported_petri
    pkg = petri.pkg
    assert pkg

    expected = {"name": "petri", "version": petri.__version__}
    for name, value in expected.items():
        assert getattr(pkg.meta, name) == value

    assert petri.__version__ == pyproject_toml["version"]
