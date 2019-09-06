from a_pkg import __meta__


def test_version():
    expected = {
        "name": "a-pkg",
        "version": "1.2.3",
        "summary": "A description",
        "author": "Author Name",
        "author_email": "author@mail.com",
    }
    for k, v in expected.items():
        assert getattr(__meta__, k) == v
