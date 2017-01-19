##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from collections import defaultdict
from itertools import chain
from os import listdir
from os import path
import yaml

from qtip.base.error import InvalidFormat, NotFound
from qtip.base.constant import BaseProp


ROOT_DIR = path.join(path.dirname(__file__), path.pardir, path.pardir,
                     'benchmarks')


class BaseLoader(object):
    """Abstract class of QTIP specification loader"""
    RELATIVE_PATH = '.'
    _paths = [ROOT_DIR]

    def __init__(self, name, paths=None):
        self._file = name
        self._abspath = self._find(name, paths=paths)
        content = defaultdict(lambda: None)

        try:
            content.update(yaml.safe_load(file(self._abspath)))
        except yaml.YAMLError:
            # TODO(yujunz) log yaml error
            raise InvalidFormat(self._abspath)

        self.name = content[BaseProp.NAME] or path.splitext(name)[0]
        self.content = content

    def _find(self, name, paths=None):
        """find a specification in searching paths"""
        paths = self._paths if paths is None else paths
        for p in paths:
            abspath = path.join(p, self.RELATIVE_PATH, name)
            if path.exists(abspath):
                return abspath
        raise NotFound(name, paths)

    @classmethod
    def list_all(cls, paths=None):
        """list all available specification"""
        paths = cls._paths if paths is None else paths
        names = chain.from_iterable([listdir(path.join(p, cls.RELATIVE_PATH))
                                     for p in paths])
        for name in names:
            item = cls(name, paths=paths)
            yield {
                BaseProp.NAME: name,
                BaseProp.ABSPATH: item._abspath,
                BaseProp.CONTENT: item.content}
