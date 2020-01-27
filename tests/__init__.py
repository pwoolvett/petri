# -*- coding: utf-8 -*-

from contextlib import AbstractContextManager
from contextlib import contextmanager
import os

@contextmanager
def temp_file(path, mode):
    file = open(path, mode)
    try:
        yield file
    finally:
        file.close()
        os.remove(path)
        
        
class nullcontext(AbstractContextManager):  # pylint: disable=invalid-name
    """Context manager that does no additional processing.

    Used as a stand-in for a normal context manager, when a particular
    block of code is only sometimes used with a normal context manager:

    cm = optional_cm if condition else nullcontext()
    with cm:
        # Perform operation, using optional_cm if condition is True
    """

    def __init__(self, enter_result=None):
        self.enter_result = enter_result

    def __enter__(self):
        return self.enter_result

    def __exit__(self, *excinfo):  # pylint: disable=W0221
        pass
