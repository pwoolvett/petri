# coding=utf-8
"""Package documentation

.. versionadded:: 0.1.0
   Initial version.

"""
import inspect
import sys

from petri import _logging_ as logging, metadata
from petri.settings import init_dotenv

logger = logging.get_logger()


def setup(filename=None):
    """

    Args:
        filename:

    Returns:

    """
    if filename:
        fn = filename
    else:
        frame_records = inspect.stack()
        fn = frame_records[2].filename
    module = {
        v.__file__: v for k, v in sys.modules.items() if getattr(v, "__file__", None)
    }[fn]

    pkg = module.__package__

    return fn, module, pkg


def init():
    """

    Returns:

    """
    fn, module, pkg = setup()
    metadata.monkey_patch_metadata(fn, module, pkg)
    s = init_dotenv(fn, module, pkg)
    logger_ = logging.gen_logger(pkg)
    return s, logger_


def init_docs():
    """

    Returns:

    """
    fn, module, pkg = setup(__file__)

    logger.info(f"Module to be patched: {module}")

    metadata.monkey_patch_metadata(fn, module, pkg)
    s = init_dotenv(fn, module, pkg)
    return s
