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

from error import InvalidFormat, NotFound
from constant import PropName

ROOT_DIR = 'benchmarks'


class Benchmark(object):
    """Abstract class of QTIP benchmarks"""
    DEFAULT_DIR = '.'
    _paths = [path.join(path.dirname(__file__), path.pardir, path.pardir,
                        ROOT_DIR)]

    def __init__(self, name, paths=None):
        self._file = name
        self._abspath = self._find(name, paths)

        try:
            content = yaml.safe_load(file(self._abspath))
        except yaml.YAMLError:
            # TODO(yujunz) log yaml error
            raise InvalidFormat(self._abspath)

        self.name = content[PropName.NAME] if PropName.NAME in content \
            else path.splitext(name)[0]
        self.content = content

    def _find(self, name, paths):
        """find a benchmark in searching paths"""
        paths = self._paths if paths is None else paths
        name = path.join(self.DEFAULT_DIR, name)
        for p in paths:
            abspath = path.join(p, name)
            if path.exists(abspath):
                return abspath
        raise NotFound(name, paths)

    @classmethod
    def list_all(cls, paths=None):
        """list all available benchmarks"""
        paths = cls._paths if paths is None else paths
        names = chain.from_iterable([listdir(path.join(p, cls.DEFAULT_DIR))
                                     for p in paths])
        for name in names:
            item = cls(name, paths=paths)
            yield {
                PropName.NAME: name,
                PropName.ABSPATH: item._abspath,
                PropName.CONTENT: item.content}
