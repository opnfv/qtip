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

METRIC_SPEC = 'fake-metric.yaml'

@pytest.fixture(scope='module')
def metric_spec(opt_root):
    return MetricSpec(METRIC_SPEC, paths=[opt_root])


def init_test(metric_spec):
    assert metric_spec.name == 'Fake Metric'

    with pytest.raises(TypeError) as excinfo:
        MetricSpec()
    assert '__init__() takes at least 2 arguments (1 given)' \
           in str(excinfo.value)


def list_all_test():
    metric_list = MetricSpec.list_all()
    assert len(list(metric_list)) is 6
    for desc in metric_list:
        assert BaseProp.NAME in desc
        assert BaseProp.DESCRIPTION in desc
        assert BaseProp.ABSPATH in desc
        assert BaseProp.ABSPATH is not None


def content_test(metric):
    content = metric.content
    assert BaseProp.NAME in content
    assert BaseProp.DESCRIPTION in content
    assert BaseProp.WORKLOADS in content
    assert isinstance(content[BaseProp.WORKLOADS], list)
