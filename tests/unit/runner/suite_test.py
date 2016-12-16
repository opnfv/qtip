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
from qtip.runner.benchmark import Property


class TestSuiteClass:
    def test_attr(self):
        assert len(Suite._paths) is 1


class TestSuite:
    Suite._paths = [path.join(path.dirname(__file__), path.pardir, path.pardir,
                              'data', 'suite')]

    def test_init(self):
        suite = Suite('suite-1.yaml')
        assert suite.name == 'suite-1.yaml'

        with pytest.raises(TypeError) as excinfo:
            Suite()
        assert '__init__() takes exactly 2 arguments (1 given)' \
               in str(excinfo.value)

    def test_list(self):
        suite_list = Suite.list_all()
        assert len(list(suite_list)) is 3
        for suite_desc in suite_list:
            assert Property.NAME in suite_desc
            assert Property.DESCRIPTION in suite_desc
            assert Property.ABSPATH in suite_desc
            assert Property.ABSPATH is not None

    @pytest.mark.parametrize("test_input, expected", [
        ('suite-1.yaml',
         {
            'name': 'suite-1.yaml',
            'abspath': str(Suite._paths[0]) + '/suite-1.yaml',
            'description': 'sample performance index of computing',
            'content': {'QPI': 'compute',
                        'description': 'sample performance index of computing'}
         }),
        ('suite-2.yaml',
         {
             'name': 'suite-2.yaml',
             'abspath': str(Suite._paths[0]) + '/suite-2.yaml',
             'description': None,
             'content': None
         })
    ])
    def test_describe(self, test_input, expected):
        suite = Suite(test_input)
        info = suite.describe()
        assert info == expected

