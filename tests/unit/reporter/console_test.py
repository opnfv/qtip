##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pickle
import pytest
import os

from qtip.reporter.console import ConsoleReporter


@pytest.fixture
def console_reporter():
    return ConsoleReporter({})


def test_constructor(console_reporter):
    assert isinstance(console_reporter, ConsoleReporter)


def test_render(console_reporter):
    types = ['report', 'sys_info', 'timeline']
    path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,
                        os.pardir, 'tests/data/reporter/')

    for i in range(0, len(types)):
        var_dict = pickle.load(open('{}{}{}{}'.format(path, 'dicts/', types[i],
                                    '.pickle'), 'rb'))
        result = console_reporter.render(var_dict, types[i])
        output = pickle.load(open('{}{}{}{}'.format(path, 'output/', types[i],
                                  '.pickle'), 'rb'))
        assert result == output
