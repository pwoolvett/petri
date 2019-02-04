#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""All things log-related: configuration, logger creation, etc
"""

import logzero


class MyFormatter(logzero.LogFormatter):
    """Define common logs formatting"""

    def __init__(self):
        fmt = "".join(
            [
                "%(color)s",
                "%(asctime)s" " %(levelname)s | ",
                "%(filename)s:%(name)s:%(funcName)s:%(lineno)d",
                "%(end_color)s" ":\n",
                "%(message)s",
            ]
        )
        datefmt = "%Y/%m/%d@%H:%M:%S"

        super(MyFormatter, self).__init__(fmt=fmt, datefmt=datefmt)


def get_logger(log_level=1):
    """Return properly formatted logger
    """

    _logger = logzero.setup_logger(
        name=__package__, level=log_level, formatter=MyFormatter()
    )

    return _logger
