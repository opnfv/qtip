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


class Property:
    NAME = 'name'
    DESCRIPTION = 'description'
    ABSPATH = 'abspath'


class Benchmark:
    """Abstract class of QTIP benchmarks"""

    _paths = [path.join(path.dirname(__file__), path.pardir, path.pardir,
                        'benchmarks')]

    def __init__(self, name):
        self.name = name
        self._abspath = self._find(name)

    def _find(self, name):
        """find a benchmark in searching paths"""
        for p in self._paths:
            abspath = path.join(p, name)
            if path.exists(abspath):
                return abspath
        return None

    @classmethod
    def list_all(cls):
        """list all available benchmarks"""
        names = chain.from_iterable([listdir(p) for p in cls._paths])
        return [Benchmark(name).describe() for name in names]

    def describe(self):
        """description of benchmark"""
        # TODO(yujunz) read description from benchmark content
        return {
            Property.NAME: self.name,
            Property.DESCRIPTION: 'QTIP benchmark',
            Property.ABSPATH: self._abspath
        }
