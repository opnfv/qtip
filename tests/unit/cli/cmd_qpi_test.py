###############################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.cli.entry import cli
from click.testing import CliRunner


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_list(runner):
    result = runner.invoke(cli, ['qpi', 'list'])
    assert 'QPIs' and 'compute' in result.output


def test_run(runner):
    result = runner.invoke(cli, ['qpi', 'run', 'fake-qpi'])
    assert result.output == ''

    result = runner.invoke(cli, ['qpi', 'run'])
    assert 'Missing argument "name".' in result.output


def test_show(runner):
    result = runner.invoke(cli, ['qpi', 'show', 'compute'])
    assert 'Name: compute' in result.output
    assert 'Description: sample performance index of computing' in result.output

    result = runner.invoke(cli, ['qpi', 'show'])
    assert 'Missing argument "name".' in result.output

    result = runner.invoke(cli, ['qpi', 'show', 'xyz'])
    assert "ERROR: qpi spec: xyz not found" in result.output
