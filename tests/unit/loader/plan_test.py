##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.collector.logfile import LogfileCollector
from qtip.loader.plan import load_collector
from qtip.loader.plan import Plan
from qtip.loader.plan import PlanProp
from qtip.loader.plan import QPISpec


def test_init(plan):
    assert plan.name == 'doctor performance profiling'
    assert isinstance(plan.content, dict)
    for qpi in plan.qpis:
        assert isinstance(qpi, QPISpec)

    with pytest.raises(TypeError) as excinfo:
        Plan()
    assert '__init__() takes at least 2 arguments (1 given)' \
           in str(excinfo.value)


def test_list_all(benchmarks_root):
    plan_list = list(Plan.list_all(paths=[benchmarks_root]))
    assert len(plan_list) is 1
    for desc in plan_list:
        assert PlanProp.NAME in desc
        assert PlanProp.ABSPATH in desc
        assert PlanProp.ABSPATH is not None


def test_content(plan):
    content = plan.content
    assert PlanProp.NAME in content
    assert PlanProp.DESCRIPTION in content
    assert PlanProp.CONFIG in content
    assert PlanProp.QPIS in content


def test_load_collector():
    assert load_collector(LogfileCollector.TYPE) is LogfileCollector
