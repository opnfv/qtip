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


@pytest.fixture
def paths():
    return os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,
                        os.pardir, 'tests/data/reporter/output/')


def test_reporter(runner, paths):

    types = ['detail.json', 'timeline.json']

    result = runner.invoke(cli, ['report', 'show'])

    for i in range(0, len(types)):
        with open('{}{}'.format(paths, types[i])) as output:
            report = json.load(output)
        assert report in result.output
