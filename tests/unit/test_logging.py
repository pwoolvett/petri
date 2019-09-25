import importlib
import itertools
import os
import sys
from contextlib import nullcontext
from pathlib import Path
import shutil

import pytest

from isort.settings import from_path
from tests.unit import a_pkg_import
from tests.unit import temp_file
from tests.unit import restore_file

def test_load_settings(monkeypatch, a_pkg_import, envalue):

    with monkeypatch.context() as patcher:
        a_pkg = a_pkg_import(setenv=False)
        