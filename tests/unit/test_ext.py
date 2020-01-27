# -*- coding: utf-8 -*-

from petri.ext import pkg_2_envvar
from petri.ext import to_upper_underscore


def test_to_upper_underscore():
    assert to_upper_underscore("a-pkg") == "A_PKG_"


def test_pkg_2_envvar():
    return pkg_2_envvar("a-pkg") == "A_PKG_CONFIG"
