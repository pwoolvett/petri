# -*- coding: utf-8 -*-

import itertools
import logging
import os
import sys

import pytest
import tqdm

from petri import loggin


@pytest.mark.parametrize(
    "dev_mode,tqdm_installed", itertools.product((*[(True, False)] * 2))
)
def test_maybe_patch_tqdm(
    dev_mode, tqdm_installed,
):
    class Mocklogger:  # pylint: disable=C0115,R0903
        def __init__(self):
            self.warnings = list()

        def warning(self, *args, **kwargs):
            self.warnings.append({"args": args, "kwargs": kwargs})

    logger = Mocklogger()

    if tqdm_installed:
        loggin.TQDM_INSTALLED = True
        loggin.maybe_patch_tqdm(logger, dev_mode)

        for _ in tqdm.tqdm(range(10)):
            pass
        assert len(logger.warnings) == (1 - int(dev_mode))
    else:
        loggin.TQDM_INSTALLED = False
        loggin.maybe_patch_tqdm(logger, dev_mode)

        for _ in tqdm.tqdm(range(10)):
            pass
        assert len(logger.warnings) == 0


def test__control_logging():
    raise NotImplementedError


def test_configure_logging():
    raise NotImplementedError


def test_trace_using():
    raise NotImplementedError
