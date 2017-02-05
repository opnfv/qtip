##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import pytest

from qtip.collector.parser import Parser


@pytest.fixture
def logfile(dataroot):
    return os.path.join(dataroot, 'fake.log')


@pytest.fixture
def grep():
    return Parser.grep


@pytest.mark.parametrize("regex,expected", [
    ('not exist', {}),
    ('Lorem (\S+)', {})
])
def grep_test(grep, logfile, regex, expected):
    group = grep(logfile, regex)
    assert group == expected
