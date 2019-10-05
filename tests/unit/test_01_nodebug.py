import itertools
import re
from pathlib import Path

import pytest

PETRI_SRC_FOLDER = Path(__file__).parent.parent.parent / "petri"

DEBUG_INDICATORS = [
    re.compile(r"{}".format(indicator))
    for indicator in (
        r"pdb",
        r"set_trace\(",
        r"embed\(",
        r"breakpoint\(",
        r"IPython",
    )
]

SRC_FILES = [str(path.resolve()) for path in PETRI_SRC_FOLDER.rglob("*.py")]


@pytest.mark.parametrize(
    "file,debug_statement", itertools.product(SRC_FILES, DEBUG_INDICATORS)
)
def test_pdb(file, debug_statement):
    with open(file, "r") as fp:
        txt = fp.read()
    assert not debug_statement.findall(txt)
