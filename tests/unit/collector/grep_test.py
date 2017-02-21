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

from qtip.collector.parser.grep import grep_in_file


@pytest.fixture
def logfile(data_root):
    return os.path.join(data_root, 'fake.log')


@pytest.mark.parametrize("regex,expected", [
    ('not exist', []),
    ('Lorem (\S+)', [{'groups': ('ipsum',), 'groupdict': {}}]),
    ('nisi ut (?P<name>\S+)', [{'groups': ('aliquip',), 'groupdict': {'name': 'aliquip'}}]),
    ('Lorem\s(\w+)\s.+\nconsectetur\s(\w+)\s.+\n',
     [{'groups': ('ipsum', 'adipiscing',), 'groupdict': {}}])
])
def test_grep_in_file(logfile, regex, expected):
    matches = grep_in_file(logfile, regex)
    assert len(matches) == len(expected)
    for i in range(len(matches)):
        assert matches[i].groups() == expected[i]['groups']
        assert matches[i].groupdict() == expected[i]['groupdict']
