from a_pkg import __meta__


def test_version():
    assert __meta__.release == "pre-alpha"
    assert __meta__.maintainer == "Maintainer Name <maintainer@mail.com>"
    assert __meta__.copyright == "A copyright"
    assert __meta__.url == "www.a_package.com"
    assert __meta__.license == "A License"
    assert __meta__.name == "a_pkg"
    assert __meta__.version == "1.2.3"
    assert __meta__.description == "A description"
    assert __meta__.readme == "README.rst"

    assert __meta__.authors == ["Author Name <author@mail.com>"]
