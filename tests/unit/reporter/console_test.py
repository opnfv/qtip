##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest
from qtip.reporter.console import ConsoleReporter


@pytest.fixture
def console_reporter():
    return ConsoleReporter({})


def test_constructor(console_reporter):
    assert isinstance(console_reporter, ConsoleReporter)


def test_render(console_reporter):
    var_dict = {
        'title': 'fake title',
        'description': 'fake description'
    }
    output = console_reporter.render(var_dict=var_dict)
    assert output == 'fake title: fake description'
