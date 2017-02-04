##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from os import path

import pytest

from qtip.loader.plan import Plan


@pytest.fixture(scope='session')
def data_root():
    return path.join(path.dirname(__file__), 'data')


@pytest.fixture(scope='session')
def benchmarks_root(data_root):
    return path.join(data_root, 'benchmarks')


@pytest.fixture(scope='session')
def plan(benchmarks_root):
    return Plan('fake-plan.yaml', [benchmarks_root])


@pytest.fixture(scope='session')
def external_root(data_root):
    return path.join(data_root, 'external')
