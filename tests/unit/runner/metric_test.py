###############################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from os import path
import pytest

from qtip.runner.metric import Metric
from qtip.runner.benchmark import Property


class TestMetricTestClass:
    def test_attr(self):
        assert len(Metric._paths) is 1


class TestMetricTest:
    Metric._paths = [path.join(path.dirname(__file__), path.pardir,
                               path.pardir, 'data', 'perftest')]

    def test_init(self):
        metric = Metric('test-a')
        assert metric.name == 'test-a'

        with pytest.raises(TypeError) as excinfo:
            Metric()
        assert '__init__() takes exactly 2 arguments (1 given)' \
               in str(excinfo.value)

    def test_list(self):
        metric_list = Metric.list_all()
        assert len(list(metric_list)) is 1
        for desc in metric_list:
            assert Property.NAME in desc
            assert Property.DESCRIPTION in desc
            assert Property.ABSPATH in desc
            assert Property.ABSPATH is not None

    def test_describe(self):
        desc = Metric('test-a').describe()
        assert Property.NAME in desc
        assert Property.DESCRIPTION in desc
        assert Property.ABSPATH in desc
