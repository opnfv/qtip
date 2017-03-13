###############################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest
from click.testing import CliRunner

from qtip.cli.entry import cli


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_list(runner):
    result = runner.invoke(cli, ['plan', 'list'])
    assert 'Plan' and 'compute' and 'sample' in result.output


def test_run(runner):
    result = runner.invoke(cli, ['plan', 'run', 'fake-plan'])
    assert result.output == ''

    result = runner.invoke(cli, ['plan', 'run'])
    assert 'Missing argument "name".' in result.output


def test_show(runner):
    result = runner.invoke(cli, ['plan', 'show', 'compute'])
    assert 'Name: compute QPI' in result.output
    assert 'Description: compute QPI profile'

    result = runner.invoke(cli, ['plan', 'show'])
    assert 'Missing argument "name".' in result.output
