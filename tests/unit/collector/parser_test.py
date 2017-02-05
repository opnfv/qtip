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

from qtip.collector.parser.grep import GrepParser


@pytest.fixture
def logfile(data_root):
    return os.path.join(data_root, 'fake.log')


@pytest.mark.parametrize("regex,expected", [
    ('not exist', None),
    ('Lorem (\S+)', {'group': 'ipsum'})
])
def grep_test(logfile, regex, expected):
    group = GrepParser.search(logfile, regex)
    assert group == expected
