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
    assert 'QPIs' in result.output


def test_show(runner):
    result = runner.invoke(cli, ['qpi', 'show', 'compute'])
    assert 'QPI' in result.output
    assert 'Description' in result.output
    assert 'Formula' in result.output
