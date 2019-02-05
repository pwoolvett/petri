import os
import sys

from . import def_stuff


def test_settings():
    import petri

    fn, module, pkg = def_stuff(__file__)

    s = petri.init_dotenv(fn, module, pkg)

    assert os.environ["OVERLOAD"] == "OLD"
    assert os.environ["ENV"] == "TEST"
    assert os.environ["LONE"] == "SAMPLE"

    assert s.OVERLOAD == "NEW"
    assert s.ENV == "TEST"
    assert s.LONE == "SAMPLE"
