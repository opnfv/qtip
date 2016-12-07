##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from itertools import chain
from os import listdir
from os import path


class SuiteProperty:
    NAME = 'name'
    DESCRIPTION = 'description'
    ABSPATH = 'abspath'


class Suite:
    """A suite is consist of one or several perf tests and produces one QPI"""

    # paths to search for suites
    _paths = [path.join(path.dirname(__file__), path.pardir, path.pardir,
                        'benchmarks', 'suite')]

    def __init__(self, name):
        """:param name: suite name"""
        # TODO(yujunz) check existence and expand to full path
        self.name = name
        self._abspath = self._find(name)

    def _find(self, name):
        """find a suite in searching paths"""
        for p in self._paths:
            abspath = path.join(p, name)
            if path.exists(abspath):
                return abspath
        return None

    @classmethod
    def list_all(cls):
        """list all available suites"""
        suite_names = chain.from_iterable([listdir(p) for p in cls._paths])
        return [Suite(name).describe() for name in suite_names]

    def describe(self):
        """description of benchmark suite"""
        # TODO(yujunz)
        # - read description from suite content
        # - verbose mode including even more details
        #   - referred perftests
        #   - formula of QPI calculation
        #   - baseline description
        return {
            SuiteProperty.NAME: self.name,
            SuiteProperty.DESCRIPTION: 'QTIP benchmark suite',
            SuiteProperty.ABSPATH: self._abspath
        }

    def run(self):
        """run included perftests in the suite"""
        pass
