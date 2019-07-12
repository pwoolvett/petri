import pytest


def test_import():
    import petri

    meta = petri.__meta__
    assert meta


def test_non_existent():
    from petri import __meta__

    with pytest.raises(AttributeError):
        __meta__.asdhjlghksd  # pylint: disable=pointless-statement
