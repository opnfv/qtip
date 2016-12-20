##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.base.benchmark import Property
from qtip.runner.case import Case
from qtip.runner.plan import Plan
from qtip.runner.suite import Suite


@pytest.fixture(scope='module')
def plan(benchmarks_root):
    return Plan('verification.yaml', paths=[benchmarks_root])


@pytest.fixture(scope='module')
def suite(plan):
    return Suite(plan[Property.SUITES][0])


@pytest.fixture(scope='module')
def case(suite):
    return Case(suite[Property.CASES][0])
