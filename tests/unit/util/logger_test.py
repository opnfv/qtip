##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.util import logger

MODULE = 'test_logger'
ERROR_MSG = 'error level test'
INFO_MSG = 'info level test'
DEBUG_MSG = 'debug level test'


@pytest.fixture()
def env_home(monkeypatch, tmpdir):
    monkeypatch.setenv('HOME', str(tmpdir))
    return tmpdir


@pytest.fixture()
def logger_file(env_home):
    return env_home.mkdir('qtip').mkdir('logs').join('{}.log'.format(MODULE))


def console_expect_debug(content):
    assert DEBUG_MSG in content


def console_expect_nodebug(content):
    assert DEBUG_MSG not in content


@pytest.mark.parametrize('debug, console_expected', [
    ('true', console_expect_debug),
    ('false', console_expect_nodebug)])
def test_logger(monkeypatch, capsys, logger_file, debug, console_expected):
    monkeypatch.setenv('IF_DEBUG', debug)

    log = logger.QtipLogger(MODULE).get
    log.error(ERROR_MSG)
    log.info(INFO_MSG)
    log.debug(DEBUG_MSG)

    file_print = logger_file.read()
    assert ERROR_MSG in file_print
    assert INFO_MSG in file_print
    assert DEBUG_MSG in file_print

    _, console_print = capsys.readouterr()

    console_expected(console_print)
