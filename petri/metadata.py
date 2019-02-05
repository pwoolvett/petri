"""Set values in ../pyproject.toml -> ["tool"]["poetry"] a dunder attribute for importing package"""
import os

import toml


class Metadata:
    def __init__(self, file):
        self.file = file
        self.storage_ = None

    @property
    def storage(self):
        if not self.storage_:
            dir_ = f"{os.path.dirname(os.path.abspath(self.file))}"
            fp = os.path.join(os.path.dirname(dir_), "pyproject.toml")
            pyproj_toml = toml.load(fp)["tool"]["poetry"]
            self.storage_ = {f"__{k}__": v for k, v in pyproj_toml.items()}

        return self.storage_

    def __getattr__(self, attr):
        val = self.storage.get(attr)
        if not val:
            raise AttributeError(f"package '{__package__}' has no attribute '{attr}'")
        return val

    __getitem__ = __getattr__

    def items(self):
        for k, v in self.storage.items():
            yield k, v


def monkey_patch_metadata(fn, module, pkg):
    meta = Metadata(module.__file__)

    for attr_name, attr_value in meta.items():
        setattr(module, attr_name, attr_value)

    return meta
