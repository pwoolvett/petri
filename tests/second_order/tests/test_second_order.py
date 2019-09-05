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

def test_lib():
    import a_pkg
    from a_pkg import my_module

    assert a_pkg.__meta__.release == "pre-alpha"
    assert a_pkg.__meta__.maintainer == "Maintainer Name <maintainer@mail.com>"
    assert a_pkg.__meta__.copyright == "A copyright"
    assert a_pkg.__meta__.url == "www.a_package.com"
    assert a_pkg.__meta__.license == "A License"
    assert a_pkg.__meta__.name == "a_pkg"
    assert a_pkg.__meta__.version == "1.2.3"
    assert a_pkg.__meta__.description == "A description"
    assert a_pkg.__meta__.readme == "README.rst"

    assert a_pkg.__meta__.authors == ["Author Name <author@mail.com>"]

    assert my_module.module_var == 'module_var'
