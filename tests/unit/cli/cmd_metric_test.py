###############################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest
from click.testing import CliRunner

from qtip.cli.entry import cli


@pytest.fixture()
def runner():
    return CliRunner()


def test_list(runner):
    result = runner.invoke(cli, ['metric', 'list'])
    assert result.output == ''


def test_run(runner):
    result = runner.invoke(cli, ['metric', 'run', 'fake-metric'])
    assert result.output == ''

    result = runner.invoke(cli, ['metric', 'run'])
    assert 'Missing argument "name".' in result.output
