import pytest

from tests.unit import a_pkg_import


@pytest.fixture(scope="function")
def read_meta(a_pkg_import):
    a_pkg = a_pkg_import()
    return a_pkg.pkg.meta


def test_meta(read_meta):
    expected = {
        "name": "a-pkg",
        "version": "1.2.3",
        "author": "Author Name",
        "author-email": "author@mail.com",
        "summary": "A description",
    }
    for name, value in expected.items():
        assert getattr(read_meta, name) == value
