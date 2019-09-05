from second_order import __meta__


def test_meta():
    assert __meta__.release == "pre-alpha"
    assert __meta__.maintainer == "Maintainer Name <maintainer@mail.com>"
    assert __meta__.copyright == "A copyright"
    assert __meta__.url == "www.second_order.com"
    assert __meta__.license == "A License"
    assert __meta__.name == "second_order"
    assert __meta__.version == "4.5.6"
    assert __meta__.description == "A description"
    assert __meta__.readme == "README.rst"

    assert __meta__.authors == ["Author Name <author@mail.com>"]
