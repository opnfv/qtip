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

from qtip.runner.perftest import PerfTest
from qtip.runner.benchmark import Property


class CheckPerfTestClass:
    def test_attr(self):
        assert len(PerfTest._paths) is 1


class CheckPerfTest:
    PerfTest._paths = [path.join(path.dirname(__file__), path.pardir,
                                 path.pardir, 'data', 'perftest')]

    def test_init(self):
        perftest = PerfTest('test-a')
        assert perftest.name == 'test-a'

        with pytest.raises(TypeError) as excinfo:
            PerfTest()
        assert '__init__() takes exactly 2 arguments (1 given)' \
               in str(excinfo.value)

    def test_list(self):
        perftest_list = PerfTest.list_all()
        assert len(list(perftest_list)) is 1
        for desc in perftest_list:
            assert Property.NAME in desc
            assert Property.DESCRIPTION in desc
            assert Property.ABSPATH in desc
            assert Property.ABSPATH is not None
