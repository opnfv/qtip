###############################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.base.constant import BaseProp
from qtip.loader.metric import MetricSpec


@pytest.fixture(scope='module')
def metric_spec(benchmarks_root):
    return MetricSpec('dhrystone.yaml', paths=[benchmarks_root])


def init_test(metric_spec):
    assert metric_spec.name == 'dhrystone'

    with pytest.raises(TypeError) as excinfo:
        MetricSpec()
    assert '__init__() takes at least 2 arguments (1 given)' \
           in str(excinfo.value)


def list_all_test(benchmarks_root):
    metric_list = list(MetricSpec.list_all(paths=[benchmarks_root]))
    assert len(metric_list) is 6
    for desc in metric_list:
        assert BaseProp.NAME in desc
        assert BaseProp.ABSPATH in desc
        assert BaseProp.ABSPATH is not None


def content_test(metric_spec):
    content = metric_spec.content
    assert BaseProp.NAME in content
    assert BaseProp.WORKLOADS in content
    assert isinstance(content[BaseProp.WORKLOADS], list)
