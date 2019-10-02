import a_pkg


def test_version():
    expected = {
        "name": "a-pkg",
        "version": "1.2.3",
        "summary": "A description",
        "author": "Author Name",
        "author-email": "author@mail.com",
    }
    for k, v in expected.items():
        assert getattr(a_pkg.pkg.meta, k) == v
