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

from qtip.base.error import InvalidFormat, NotFound
from qtip.base.constant import PropName


ROOT_DIR = path.join(path.dirname(__file__), path.pardir, path.pardir,
                     'benchmarks')


class BaseLoader(object):
    """Abstract class of QTIP benchmark loader"""
    RELATIVE_PATH = '.'
    _paths = [ROOT_DIR]

    def __init__(self, name, paths=None):
        self._file = name
        self._abspath = self._find(name, paths=paths)

        try:
            content = yaml.safe_load(file(self._abspath))
        except yaml.YAMLError:
            # TODO(yujunz) log yaml error
            raise InvalidFormat(self._abspath)

        self.name = content[PropName.NAME] if PropName.NAME in content \
            else path.splitext(name)[0]
        self.content = content

    def _find(self, name, paths=None):
        """find a benchmark in searching paths"""
        paths = self._paths if paths is None else paths
        for p in paths:
            abspath = path.join(p, self.RELATIVE_PATH, name)
            if path.exists(abspath):
                return abspath
        raise NotFound(name, paths)

    @classmethod
    def list_all(cls, paths=None):
        """list all available benchmarks"""
        paths = cls._paths if paths is None else paths
        names = chain.from_iterable([listdir(path.join(p, cls.RELATIVE_PATH))
                                     for p in paths])
        for name in names:
            item = cls(name, paths=paths)
            yield {
                PropName.NAME: name,
                PropName.ABSPATH: item._abspath,
                PropName.CONTENT: item.content}
