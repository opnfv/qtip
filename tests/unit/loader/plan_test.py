##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.base.constant import PlanProp
from qtip.loader.plan import Plan, QPISpec


def test_init(plan):
    assert plan.name == 'Fake Plan'
    assert isinstance(plan.content, dict)
    for qpi in plan.qpis:
        assert isinstance(qpi, QPISpec)

    with pytest.raises(TypeError) as excinfo:
        Plan()
    assert '__init__() takes at least 2 arguments (1 given)' \
           in str(excinfo.value)


def test_list_all(opt_root):
    plan_list = Plan.list_all(paths=[opt_root])
    assert len(list(plan_list)) is 1
    for desc in plan_list:
        assert PlanProp.NAME in desc
        assert PlanProp.CONTENT in desc
        assert PlanProp.ABSPATH in desc
        assert PlanProp.ABSPATH is not None


def test_content(plan):
    content = plan.content
    assert PlanProp.NAME in content
    assert PlanProp.DESCRIPTION in content
    assert PlanProp.CONFIG in content
    assert PlanProp.QPIS in content
