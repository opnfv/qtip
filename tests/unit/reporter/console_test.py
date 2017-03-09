##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
import pytest
import os

from qtip.reporter.console import ConsoleReporter


@pytest.fixture
def console_reporter():
    return ConsoleReporter({})


@pytest.fixture
def paths():
    return os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,
                        os.pardir, 'tests/data/reporter/')


def test_constructor(console_reporter):
    assert isinstance(console_reporter, ConsoleReporter)


def test_details(console_reporter, paths):

    types = ['detail.json', 'timeline.json']

    for kind in types:
        """ Load var_dict """
        with open('{}{}{}'.format(paths, 'dicts/', kind)) as sample:
            data = json.load(sample)
        result = console_reporter.render(data, kind[0:-5])

        """ Load expected output"""
        with open('{}{}{}'.format(paths, 'output/', kind)) as output:
            report = json.load(output)

        assert result == report
