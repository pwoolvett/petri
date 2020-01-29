# -*- coding: utf-8 -*-

import itertools
import logging
import os
import sys
from pathlib import Path

import pytest
import tqdm
from structlog import get_logger
from structlog.testing import capture_logs

from petri import loggin
from tests import temp_file


def warnings(cap_logs_):
    return [event for event in cap_logs_ if event["log_level"] == "warning"]


@pytest.mark.parametrize(
    "dev_mode,tqdm_installed", itertools.product((*[(True, False)] * 2))
)
def test_maybe_patch_tqdm(
    dev_mode, tqdm_installed,
):

    with capture_logs() as cap_logs:
        logger = get_logger()

        if tqdm_installed:
            loggin.TQDM_INSTALLED = True
            loggin.maybe_patch_tqdm(logger, dev_mode)

            for _ in tqdm.tqdm(range(10)):
                pass
            assert len(warnings(cap_logs)) == 1 - int(dev_mode)
        else:
            loggin.TQDM_INSTALLED = False
            loggin.maybe_patch_tqdm(logger, dev_mode)

            for _ in tqdm.tqdm(range(10)):
                pass
            assert len(warnings(cap_logs)) == 0


class TestControlLogging:
    @classmethod
    def make_logger(cls, name, force=False, **kwargs):
        log_settings = {
            "level": kwargs.pop("level", loggin.LogLevel.TRACE),
            "dest": kwargs.pop("dest", loggin.LogDest.CONSOLE),
            "formatter": kwargs.pop("formatter", loggin.LogFormatter.JSON),
            "log_file": "asdf",
        }
        return loggin.configure_logging(
            name, log_settings=log_settings, force=force
        )

    def test_should_not_kidnap(self, caplog):
        library_log = self.make_logger("library", log_level=50)
        application_log = self.make_logger("application", log_level=1)
        library_log.debug("this messsage should not exist")
        application_log.debug("this messsage should exist")
        assert caplog.records

    def test_should_kidnap(self, caplog):
        library_log = self.make_logger("library", log_level=50)
        application_log = self.make_logger(
            "application", log_level=1, force=True
        )
        library_log.debug("this messsage should not exist")
        application_log.debug("this messsage should exist")
        assert caplog.records


def test_configure_logging():
    raise NotImplementedError


def test_trace_using():
    raise NotImplementedError
