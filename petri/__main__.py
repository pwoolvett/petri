# coding=utf-8
"""Handle petri calls."""

import sys

import petri


if __name__ == "__main__":
    a1 = sys.argv[1]
    if a1.startswith('--'):
        print(getattr(petri.__meta__, a1[2:]))
