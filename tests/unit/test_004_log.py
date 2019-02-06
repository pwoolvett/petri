import os
import sys


def test_log():
    import petri

    petri.init()

    import petri

    settings, logger = petri.init()

    logger.debug("hello")
    logger.info("info")
    logger.warning("warning")
    logger.exception(BaseException('Except this '))
    logger.error("error")
