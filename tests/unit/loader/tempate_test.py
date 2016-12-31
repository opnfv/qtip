##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.loader.template import Template

TEMPLATE = 'console'


@pytest.fixture()
def template(benchmarks_root):
    return Template(TEMPLATE, paths=[benchmarks_root])


def test_init(template):
    assert template.name == TEMPLATE

    with pytest.raises(TypeError) as excinfo:
        Template()
    assert '__init__() takes at least 2 arguments (1 given)' \
        in str(excinfo.value)


@pytest.fixture
def timeline():
    return """\
Fake Timeline
=============
PREPARE TIME
------------
init    10ms
config  21ms
-------
RUNNING
-------
CLEANUP
-------
destroy
"""
