#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Global testing setup

Activate common pytest patterns and set environment variables:

  * New decorator-flag pair: `@pytest.mark.slow` and `--runslow`.
  * New decorator: `@pytest.mark.incremental`.
  * Define location of the `.env` file to be `tests/.env.test`.

"""

import pytest

from tests import define_test_dotenv


def pytest_addoption(parser):
    """Adds a `--runslow` command line option to control skipping of
    :code:`@pytest.mark.slow` marked tests.
    """
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_collection_modifyitems(config, items):
    """Control skipping of tests according to command line option

    Adds a `--runslow` command line option to control skipping of
    :code:`@pytest.mark.slow` marked tests.

    Example::
        $ print(open('test_skip.py','r').read())
          import pytest

          @pytest.mark.slow
          def test_skippable():
              pass

          def test_always():
              pass
        >>> import pytest
        >>> pytest.main(['-rap','test_skip.py'])
            =================== test session starts ====================
            ...
            collected 2 items
            ...
            testmodule.py s.                                      [100%]
            ================= short test summary info ==================
            SKIPPED [1] test_skip.py:3: need --runslow option to run
            PASSED test_module.py::test_always
            ...
        >>> pytest.main(['-rap', '--runslow', 'test_skip.py'])
            =================== test session starts ====================
            ...
            collected 2 items
            ...
            testmodule.py s.                                      [100%]
            ================= short test summary info ==================
            PASSED test_module.py::test_skippable
            PASSED test_module.py::test_always
            ...
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

    Abort tests within a `@pytest.mark.incremental`-decorated class if
    previous test failed.

    Example::

        Notice `test_wont_run` is not executed because `test_error`
        failed. `test_wont_run` is reported as an “expected failure”.

        >>> print(open('test_incremental.py','r').read())
        import pytest


        @pytest.mark.incremental
        class TestUserHandling:
            def test_ok(self):
                assert True

            def test_error(self):
                assert False

            def test_wont_run(self):
                assert False


        def test_ok2():
            assert True


        def test_error2():
            assert False
        >>> import pytest
        >>> pytest.main(['-s','-qqq','-rfEsxXpP','test_incremental.py'])
            ...
            ================= short test summary info ==================
            FAILED test_incremental.py::TestUserHandling::test_error
            FAILED test_incremental.py::test_error2
            XFAIL test_incremental.py::TestUserHandling::test_wont_run
              reason: Previous test failed (previousfailed.name)
            PASSED test_incremental.py::TestUserHandling::test_ok
            PASSED test_incremental.py::test_ok2

    """
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail(f"Previous test failed (previousfailed.name)")


def pytest_runtest_makereport(item, call):
    """Report method reusult status to class object for incremental."""
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item  # pylint: disable=protected-access


def pytest_configure(config):  # pylint: disable=missing-docstring,
    define_test_dotenv()
    config.addinivalue_line(
        "markers", "slow: mark test to skip unless --runslow is received."
    )
    return config


def pytest_unconfigure(config):  # pylint: disable=missing-docstring,
    return config
