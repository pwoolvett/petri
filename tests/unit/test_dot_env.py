# -*- coding: utf-8 -*-

import itertools
import os
from pathlib import Path

import pytest

from tests import nullcontext
from tests import temp_file

PWD_LOCATION = str(Path(os.getcwd()).joinpath(".env"))
CUSTOM_LOCATION = "sadfsdasdf.env"

ENV_FILE_OPTS = (None, PWD_LOCATION, CUSTOM_LOCATION)


@pytest.mark.parametrize(
    "requested,real", itertools.product(ENV_FILE_OPTS, ENV_FILE_OPTS)
)
def test_dotenv(monkeypatch, requested, real):  # pylint: disable=W0621

    from petri.dot_env import init_dotenv

    env_file_path = temp_file(real, "w+") if real else nullcontext()

    with env_file_path as real_file, monkeypatch.context() as patcher:

        if requested:
            patcher.setenv("env_file", requested)
        else:
            patcher.delenv("env_file", raising=False)

        if real:
            real_file.write("FILE_LOCATED_AT={}\n".format(real))
            real_file.seek(0)

        if requested:
            if real == requested:
                generated_location = init_dotenv()
                assert generated_location == requested
            else:
                with pytest.raises(IOError):
                    init_dotenv()
        else:  # not requested
            if real == PWD_LOCATION:
                generated_location = init_dotenv()
                assert generated_location == real
            else:
                assert init_dotenv() is None
