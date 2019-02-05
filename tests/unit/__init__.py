"""unit is a package"""
import sys


def def_stuff(__file__):
    fn = __file__
    module = {
        v.__file__: v for k, v in sys.modules.items() if getattr(v, "__file__", None)
    }[fn]
    pkg = module.__package__

    return fn, module, pkg
