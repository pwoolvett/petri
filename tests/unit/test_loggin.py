# -*- coding: utf-8 -*-

import itertools
import logging
import os
import sys
from pathlib import Path

import pytest
import tqdm

from petri import loggin
from tests import Mocklogger
from tests import temp_file


@pytest.mark.parametrize(
    "dev_mode,tqdm_installed", itertools.product((*[(True, False)] * 2))
)
def test_maybe_patch_tqdm(
    dev_mode, tqdm_installed,
):

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


class Test_ControlLogging:
    def make_logger(self, name, log_file, kidnap_loggers=False, **kwargs):
        log_settings = {
            "level": kwargs.pop("level", loggin.LogLevel.TRACE),
            "dest": kwargs.pop("dest", loggin.LogDest.FILE),
            "formatter": kwargs.pop("formatter", loggin.LogFormatter.JSON),
            "log_file": log_file,
        }
        return loggin.configure_logging(
            name, log_settings=log_settings, kidnap_loggers=kidnap_loggers
        )

    def test_should_not_kidnap(self):
        lib_m = temp_file("library.log", "w+")
        app_m = temp_file("application.log", "w+")
        with lib_m as lib_loc, app_m as app_loc:
            library_log = self.make_logger("library", lib_loc, log_level=50)
            application_log = self.make_logger(
                "application", app_loc, log_level=1
            )
            library_log.debug("this messsage should not exist")
            application_log.debug("this messsage should exist")
            import pdb

            pdb.set_trace()
            raise NotImplementedError

    def test_should_kidnap(self):
        raise NotImplementedError


def test_configure_logging():
    raise NotImplementedError


def test_trace_using():
    raise NotImplementedError
