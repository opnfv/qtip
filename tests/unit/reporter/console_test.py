##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest
from os import path

from qtip.reporter.console import ConsoleReporter


@pytest.fixture
def console_reporter():
    return ConsoleReporter({})


@pytest.fixture
def result_path():
    result = path.join(path.dirname(__file__), path.pardir, path.pardir,
                       'data/reporter')
    return result


def test_constructor(console_reporter):
    assert isinstance(console_reporter, ConsoleReporter)


@pytest.mark.parametrize(['template_name'], [
    ('dhrystone',),
    ('whetstone',),
    ('dpi',),
    ('ramspeed',),
    ('ssl',)
])
def test_templates(template_name, console_reporter, result_path):
    """ Test dhrystone report"""

    result = console_reporter.render(template_name, result_path)
    for line in result.split('\n'):
        assert len(line) <= 80
