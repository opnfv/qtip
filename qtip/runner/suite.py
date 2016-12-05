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


class Suite:
    """A suite is consist of one or several perf tests and produces one QPI"""

    # paths to search for suites
    _paths = [path.join(path.dirname(__file__), path.pardir, path.pardir,
                        'benchmarks', 'suite')]

    def __init__(self, name):
        """:param name: suite name"""
        # TODO(yujunz) check existence and expand to full path
        self.name = name

    @classmethod
    def list_all(cls):
        """list all available suites"""
        # TODO(yujunz) return name and description of suite
        return chain.from_iterable([listdir(p) for p in cls._paths])

    def desc(self):
        """description of the suite"""
        pass

    def run(self):
        """run included perftests in the suite"""
        pass
