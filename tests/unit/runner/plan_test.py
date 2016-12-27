##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.base.constant import PropName
from qtip.runner.plan import Plan


def test_init(plan):
    assert plan.name == 'fake plan'

    with pytest.raises(TypeError) as excinfo:
        Plan()
    assert '__init__() takes at least 2 arguments (1 given)' \
           in str(excinfo.value)


def test_list_all(benchmarks_root):
    plan_list = Plan.list_all(paths=[benchmarks_root])
    assert len(list(plan_list)) is 1
    for desc in plan_list:
        assert PropName.NAME in desc
        assert PropName.CONTENT in desc
        assert PropName.ABSPATH in desc
        assert PropName.ABSPATH is not None


def test_content(plan):
    content = plan.content
    assert PropName.NAME in content
    assert PropName.DESCRIPTION in content
