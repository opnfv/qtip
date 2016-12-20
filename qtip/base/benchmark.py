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
import yaml


class Property(object):
    # list
    NAME = 'name'
    CONTENT = 'content'
    ABSPATH = 'abspath'
    # content
    TITLE = 'title'
    DESCRIPTION = 'description'
    # spec
    ALGORITHM = 'algorithm'
    SECTIONS = 'sections'
    WEIGHT = 'weight'
    METRICS = 'metrics'
    TOOL = 'tool'
    WORKLOADS = 'workloads'
    # plan
    INFO = 'info'
    FACILITY = 'facility'
    ENGINEER = 'engineer'
    SUITES = 'suites'
    # suite
    QPI = 'QPI'
    CONDITION = 'condition'
    CASES = 'cases'
    # case
    METRIC = 'metric'
    CONFIG = 'config'


class QtipError(Exception):
    pass


class Algorithm(object):
    ARITHMETIC_MEAN = 'arithmetic mean'
    WEIGHTED_ARITHMETIC_MEAN = 'weighted arithmetic mean'
    GEOMETRIC_MEAN = 'geometric mean'
    WEIGHTED_GEOMETRIC_MEAN = 'weighted geometric mean'


ROOT_DIR = 'benchmarks'


class Benchmark(object):
    """Abstract class of QTIP benchmarks"""
    DEFAULT_DIR = '.'
    _paths = [path.join(path.dirname(__file__), path.pardir, path.pardir,
                        ROOT_DIR)]

    def __init__(self, name, paths=None):
        self._file = name
        self._abspath = self._find(name, paths)
        self.name = path.splitext(name)[0]

    def _find(self, name, paths):
        """find a benchmark in searching paths"""
        paths = self._paths if paths is None else paths
        name = path.join(self.DEFAULT_DIR, name)
        for p in paths:
            abspath = path.join(p, name)
            if path.exists(abspath):
                return abspath
        raise QtipError("'{}' not found in paths: {}".format(name, paths))

    @classmethod
    def list_all(cls, paths=None):
        """list all available benchmarks"""
        paths = cls._paths if paths is None else paths
        names = chain.from_iterable([listdir(path.join(p, cls.DEFAULT_DIR))
                                     for p in paths])
        for name in names:
            item = cls(name, paths=paths)
            yield {
                Property.NAME: name,
                Property.ABSPATH: item._abspath,
                Property.CONTENT: item.content()}

    def content(self):
        """description of benchmark"""
        return yaml.safe_load(file(self._abspath))
