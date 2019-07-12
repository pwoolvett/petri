# coding=utf-8
"""Handle petri calls."""

import sys

import petri


def _main():
    argv = sys.argv
    if len(argv) > 1:
        a_1 = argv[1]
        if a_1.startswith("--"):
            print(getattr(petri.__meta__, a_1[2:]))
            return

    print(petri.__doc__)


if __name__ == "__main__":
    _main()
