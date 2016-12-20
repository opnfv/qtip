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
from qtip.runner.plan import Plan


def test_init(plan):
    assert plan.name == 'verification'

    with pytest.raises(TypeError) as excinfo:
        Plan()
    assert '__init__() takes at least 2 arguments (1 given)' \
           in str(excinfo.value)


def test_list_all(benchmarks_root):
    plan_list = Plan.list_all(paths=[benchmarks_root])
    assert len(list(plan_list)) is 1
    for desc in plan_list:
        assert Property.NAME in desc
        assert Property.CONTENT in desc
        assert Property.ABSPATH in desc
        assert Property.ABSPATH is not None


def test_content(plan):
    content = plan.content()
    assert Property.TITLE in content
    assert Property.DESCRIPTION in content
