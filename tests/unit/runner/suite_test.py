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

from qtip.runner.suite import Suite
from qtip.runner.suite import SuiteProperty as SProp


class TestSuiteClass:
    def test_attr(self):
        assert len(Suite._paths) is 1


class TestSuite:
    Suite._paths = [path.join(path.dirname(__file__), path.pardir, path.pardir,
                              'data', 'suite')]

    def test_init(self):
        suite = Suite('suite-1')
        assert suite.name == 'suite-1'

        with pytest.raises(TypeError) as excinfo:
            Suite()
        assert '__init__() takes exactly 2 arguments (1 given)' \
               in str(excinfo.value)

    def test_list(self):
        suite_list = Suite.list_all()
        assert len(list(suite_list)) is 3
        for suite_desc in suite_list:
            assert SProp.NAME in suite_desc
            assert SProp.DESCRIPTION in suite_desc
            assert SProp.ABSPATH in suite_desc
