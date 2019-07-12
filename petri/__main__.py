# coding=utf-8
"""Handle petri calls."""

import sys

import petri


if __name__ == "__main__":
    if "--version" in sys.argv:
        print(petri.__meta__.version)
