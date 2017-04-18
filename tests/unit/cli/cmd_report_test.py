###############################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest
from os import path

from click.testing import CliRunner
from qtip.cli.entry import cli


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


@pytest.fixture(scope="module")
def result_path():
    result = path.join(path.dirname(__file__), path.pardir, path.pardir,
                       'data/reporter')
    return result


@pytest.mark.parametrize(['report_name'], [
    ('dhrystone',),
    ('whetstone',),
    ('dpi',),
    ('ramspeed',),
    ('ssl',)
])
def test_dhrystone(report_name, runner, result_path):
    """Test dhrystone report"""

    result = runner.invoke(cli, ['report', 'show', report_name, '-p', result_path])
    for line in str(result).split('\n'):
        assert len(line) <= 80
