# -*- coding: utf-8 -*-
"""Test package for petri"""

import os
from pathlib import Path


def define_test_dotenv():
    """Ensures `.env.test is` loaded as default"""
    dotenv_location = str(Path(__file__).parent.joinpath(".env.test"))
    os.environ["DOTENV_LOCATION"] = dotenv_location
