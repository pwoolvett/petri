#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Global testing setup

Activate common pytest patterns and set environment variables:

  * New decorator: decorador :func:`@pytest.mark.slow` and new flag :code:`--runslow` to the tests.
  * New decorator: :func:`@pytest.mark.incremental` which enables early falure for incremental tests.
  * Define location of the `.env` file to be `tests/.env.test`.

"""
import os

import pytest


def pytest_addoption(parser):
    """Adds a `--runslow` command line option to control skipping of
    :code:`@pytest.mark.slow` marked tests.
    """
    parser.addoption(
        "--runslow",
        action="store_true",
        default=False,
        help="run slow tests"
    )


def pytest_collection_modifyitems(config, items):
    """Control skipping of tests according to command line option

    Adds a `--runslow` command line option to control skipping of
    :code:`@pytest.mark.slow` marked tests.

    Example:

        .. code-block:: python

            # Content of test_module.py:
            import pytest


            def test_func_fast():
                pass


            @pytest.mark.slow
            def test_func_slow():
                from time import sleep
                sleep(500)

        When running it will see a skipped “slow” test::

          $ pytest -rs    # "-rs" means report details on the little 's'
          =========================== test session starts ============================
          platform linux -- Python 3.x.y, pytest-3.x.y, py-1.x.y, pluggy-0.x.y
          rootdir: $REGENDOC_TMPDIR, inifile:
          collected 2 items

          test_module.py .s                                                    [100%]
          ========================= short test summary info ==========================
          SKIP [1] test_module.py:8: need --runslow option to run

          =================== 1 passed, 1 skipped in 0.12 seconds ====================

        Or run it including the slow marked test::

          $ pytest --runslow
          =========================== test session starts ============================
          platform linux -- Python 3.x.y, pytest-3.x.y, py-1.x.y, pluggy-0.x.y
          rootdir: $REGENDOC_TMPDIR, inifile:
          collected 2 items

          test_module.py ..                                                    [100%]

          ========================= 2 passed in 0.12 seconds =========================

    """
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


def pytest_runtest_setup(item):
    """Incremental testing - test steps : setup

    Abort incremental-marked tests in a class if previous test failed.

    @pytest.mark.incremental

     Example:

        .. code-block:: python

            # content of test_step.py
            import pytest


            @pytest.mark.incremental
            class TestUserHandling(object):
                def test_login(self):
                    pass

                def test_modification(self):
                    assert 0

                def test_deletion(self):
                    pass


            def test_normal():
                pass

        If we run this::

          $ pytest -rx
          =========================== test session starts ============================
          platform linux -- Python 3.x.y, pytest-3.x.y, py-1.x.y, pluggy-0.x.y
          rootdir: $REGENDOC_TMPDIR, inifile:
          collected 4 items

          test_step.py .Fx.                                                    [100%]

          ================================= FAILURES =================================
          ____________________ TestUserHandling.test_modification ____________________

          self = <test_step.TestUserHandling object at 0xdeadbeef>

              def test_modification(self):
          >       assert 0
          E       assert 0

          test_step.py:11: AssertionError
          ========================= short test summary info ==========================
          XFAIL test_step.py::TestUserHandling::()::test_deletion
            reason: previous test failed (test_modification)
          ============== 1 failed, 2 passed, 1 xfailed in 0.12 seconds ===============

        We’ll see that test_deletion was not executed because test_modification failed.
        It is reported as an “expected failure”.

    """
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail(f"Previous test failed (previousfailed.name)")


def pytest_runtest_makereport(item, call):
    """Incremental testing - test steps : report status to class object."""
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_configure(config):
    dotenv_location = "tests/.env.test"
    os.environ["DOTENV_LOCATION"] = dotenv_location
    if os.path.isfile(dotenv_location):
        os.remove(dotenv_location)

    return config


def pytest_unconfigure(config):

    return config
