##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from os import path

from qtip.runner.suite import Suite


class TestSuite:
    root = path.join(path.dirname(__file__), path.pardir, path.pardir,
                     'data')

    def test_default_root(self):
        suite = Suite()
        assert suite.root.endswith('benchmarks')

    def test_root(self):
        suite = Suite(root=self.root)
        assert suite.root.endswith(path.join('data'))

    def test_list(self):
        assert True
