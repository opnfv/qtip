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
    assert len(list(plan_list)) is 2
    for desc in plan_list:
        assert PropName.NAME in desc
        assert PropName.CONTENT in desc
        assert PropName.ABSPATH in desc
        assert PropName.ABSPATH is not None


def test_content(plan):
    content = plan.content
    assert PropName.NAME in content
    assert PropName.DESCRIPTION in content
    assert PropName.CONFIG in content
    assert PropName.QPIS in content
