import datetime
import itertools
import json
import logging
from pathlib import Path

import pytest

from petri.loggin import LogDest
from petri.loggin import LogFormatter
from petri.loggin import LogLevel
from tests.unit import a_pkg_import  # pylint: disable=W0611

LEVELS = [a.value for a in dict(LogLevel.__members__).values()]
MSG_LEVELS = [
    member.lower()
    for member in LogLevel.__members__
    if member.lower() not in {"trace", "notset"}
]
DESTS = [a.value for a in dict(LogDest.__members__).values()]
FORMATTERS = [a.value for a in dict(LogFormatter.__members__).values()]


def check_log(
    msg, outerr, lvl, msg_lvl, dest, fmt, logfile_location, old_logdata
):
    out, err = outerr
    should_log = logging._nameToLevel[msg_lvl.upper()] >= lvl
    if dest == "CONSOLE":
        if should_log:
            assert out == ""
            assert msg_lvl in err
            assert msg_lvl in msg
            if fmt == "JSON":
                for line in err.splitlines():
                    assert json.loads(line)
            else:
                assert (
                    "".join(
                        x for x in err.replace(msg, "").split(" ")[1:] if x
                    )
                    .replace(msg_lvl, "")
                    .replace("a_pkg", "")
                    == "[][]\n"
                )
        else:
            assert out == ""
            assert err == ""
    elif dest == "FILE":
        assert out == ""
        assert err == ""

        with open(logfile_location, "r") as logfile:
            logdata = logfile.read()
        logdata = logdata.replace(old_logdata, "")
        Path(logfile_location).unlink()

        if should_log:
            assert msg_lvl in logdata
            if fmt == "JSON":
                assert [json.loads(line) for line in logdata.splitlines()]
            else:
                assert (
                    "".join(
                        x for x in logdata.replace(msg, "").split(" ")[1:] if x
                    )
                    .replace(msg_lvl, "")
                    .replace("a_pkg", "")
                    == "[][]\n"
                )
        else:
            assert not logdata
        return
    else:
        raise NotImplementedError


@pytest.mark.parametrize(
    "lvl,msg_lvl,dest,fmt",
    itertools.product(LEVELS, MSG_LEVELS, DESTS, FORMATTERS),
)  # pylint: disable=R0914
def test_loglevel_format_output(
    monkeypatch,
    capsys,
    a_pkg_import,  # pylint: disable=W0621
    tmpdir,
    lvl,
    msg_lvl,
    dest,
    fmt,
):

    txt = "IMPOSSIBRU! .,-'{}'-,."

    with monkeypatch.context() as patcher:
        patcher.setenv("A_PKG_LOG_LEVEL", str(lvl))
        patcher.setenv("A_PKG_LOG_DEST", dest)
        patcher.setenv("A_PKG_LOG_FORMAT", fmt)
        if dest == "FILE":
            logfile_location = tmpdir.join(
                str(datetime.datetime.now()) + ".log"
            )
            patcher.setenv("A_PKG_LOG_STORAGE", str(logfile_location))
        else:
            logfile_location = None

        a_pkg = a_pkg_import(setenv=True)

        log = a_pkg.pkg.log

        msg = txt.format(msg_lvl)

        capsys.readouterr()
        if logfile_location:
            with open(logfile_location, "r") as logfile:
                logdata = logfile.read()
        else:
            logdata = None
        getattr(log, msg_lvl)(msg)

        check_log(
            msg,
            capsys.readouterr(),
            lvl,
            msg_lvl,
            dest,
            fmt,
            logfile_location,
            logdata,
        )


def test_trace(monkeypatch, capsys, a_pkg_import):  # pylint: disable=W0621
    with monkeypatch.context() as patcher:
        patcher.setenv("A_PKG_LOG_LEVEL", "1")
        patcher.setenv("A_PKG_LOG_DEST", LogDest.CONSOLE.value)
        patcher.setenv("A_PKG_LOG_FORMAT", LogFormatter.JSON.value)

        a_pkg = a_pkg_import(setenv=True)
        log = a_pkg.pkg.log

        @log.trace
        def repeat(a, b=2, c="", d=1):  # pylint: disable=C0103
            return (a * b) + (c * d)

        capsys.readouterr()
        repeat("w", 3, c="no", d=2)
        _, err = capsys.readouterr()
        pre, post = (json.loads(line) for line in err.splitlines())

        assert pre["repr"] == "test_trace.<locals>.repeat('w',3,c='no',d=2)"
        assert post["repr"] == pre["repr"]

        assert pre["uuid"] == post["uuid"]

        assert pre["func"] == "test_trace.<locals>.repeat"
        assert post["func"] == pre["func"]

        assert set(pre["args"]) == set(["w", 3])
        assert set(pre["args"]) == set(post["args"])

        kwargs = {"c": "no", "d": 2}
        for k, v in kwargs.items():
            assert pre["kwargs"][k] == v
            assert post["kwargs"][k] == v

        assert pre["event"] == "CALLED"
        assert post["event"] == "RETURN"

        assert pre["logger"] == "a_pkg"
        assert post["logger"] == "a_pkg"

        assert pre["level"] == "info"
        assert post["level"] == "info"

        assert post["timestamp"] > pre["timestamp"]
