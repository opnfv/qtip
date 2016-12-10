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

from qtip.runner.testplan import TestPlan
from qtip.runner.benchmark import Property


class CheckTestPlanClass:
    def test_attr(self):
        assert len(TestPlan._paths) is 1


class CheckTestPlan:
    TestPlan._paths = [path.join(path.dirname(__file__), path.pardir,
                                 path.pardir, 'data', 'testplan')]

    def test_init(self):
        plan = TestPlan('plan-a')
        assert plan.name == 'plan-a'

        with pytest.raises(TypeError) as excinfo:
            TestPlan()
        assert '__init__() takes exactly 2 arguments (1 given)' \
               in str(excinfo.value)

    def test_list(self):
        plan_list = TestPlan.list_all()
        assert len(list(plan_list)) is 5
        for desc in plan_list:
            assert Property.NAME in desc
            assert Property.DESCRIPTION in desc
            assert Property.ABSPATH in desc
            assert Property.ABSPATH is not None
