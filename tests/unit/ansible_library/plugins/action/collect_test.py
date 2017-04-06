##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.ansible_library.plugins.action import collect


@pytest.fixture
def string():
    return """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""


@pytest.mark.parametrize("patterns,expected", [
    ('not exist', {}),
    ('Lorem (\S+)', {}),
    ('nisi ut (?P<name>\S+)', {'name': ['aliquip']}),
    ('in\s(?P<in>\w+)', {'in': ['reprehenderit', 'voluptate', 'culpa']})
])
def test_collect(patterns, string, expected):
    assert collect.collect(patterns, string) == expected
