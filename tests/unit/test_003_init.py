import os
import sys


def test_init():
    import petri

    petri.init()

    import petri

    s = petri.init()

    assert os.environ["OVERLOAD"] == "OLD"
    assert os.environ["ENV"] == "TEST"
    assert os.environ["LONE"] == "SAMPLE"

    assert s.OVERLOAD == "NEW"
    assert s.ENV == "TEST"
    assert s.LONE == "SAMPLE"

    assert __version__ == "0.1.0"
