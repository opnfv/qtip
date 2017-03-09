###############################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
import pytest
import os

from click.testing import CliRunner
from qtip.cli.entry import cli


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_reporter(runner):

    result = runner.invoke(cli, ['report', 'show'])

    assert "\n\nMONITORTIME\n\nT00" in result.output
    assert "1\n\n\nINSPECTORTIME\n\nT01" in result.output
    assert "\n\n\nCONTROLLERTIME\n\n" in result.output

    assert "Index: 0.0" in result.output
    assert "Plan: opnfv" in result.output
    assert "Start Time: 2017-02-24T14:48:44.543746" in result.output
    assert "Stop Time: 2017-02-24T15:48:44.543746" in result.output
    assert "CPU Usage: 3.0%" in result.output
    assert "Host Name: node-6.zte.com.cn" in result.output
    assert "Name: dpi" in result.output
    assert "Index: 95" in result.output
