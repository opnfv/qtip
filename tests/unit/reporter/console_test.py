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
    var_dict = {'title': 'Timeline', 'total': '312ms', 'phases': [{'name': 'Monitor ',
                'checkpoints': [{'name': 'T00 ', 'timestamp': '1'}]},
               {'name': 'Inspector ', 'checkpoints': [{'name': 'T01 ', 'timestamp': '2'},
                {'name': 'T02 ', 'timestamp': '5'}, {'name': 'T03 ', 'timestamp': '8'}]},
               {'name': 'Controller ', 'checkpoints': [{'name': 'T04 ', 'timestamp': '11'}]},
               {'name': 'Notifier ', 'checkpoints': [{'name': 'T05 ', 'timestamp': '16'}]},
               {'name': 'Evaluator ', 'checkpoints': [{'name': 'T06 ', 'timestamp': '40'}]}]}
    result = console_reporter.render(var_dict=var_dict)
    assert 'Timeline' and '312ms' in result
