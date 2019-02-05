import os
import sys

from . import def_stuff


def test_metadata():
    import petri

    fn, module, pkg = def_stuff(__file__)
    petri.metadata.monkey_patch_metadata(fn, module, pkg)

    assert __version__ == "0.1.0"
