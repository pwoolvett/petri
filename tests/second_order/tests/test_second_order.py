import second_order


def test_meta():
    expected = {
        "name": "second-order",
        "version": "4.5.6",
        "summary": "A description",
        "author": "Author Name",
        "author_email": "author@mail.com",
    }
    for k, v in expected.items():
        assert getattr(second_order.__meta__, k) == v


def test_lib():
    import a_pkg
    from a_pkg import my_module

    expected = {
        "name": "a-pkg",
        "version": "1.2.3",
        "summary": "A description",
        "author": "Author Name",
        "author_email": "author@mail.com",
    }
    for k, v in expected.items():
        assert getattr(a_pkg.__meta__, k) == v

    assert my_module.module_var == "module_var"
