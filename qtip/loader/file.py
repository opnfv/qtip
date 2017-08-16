##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from itertools import chain
from os import listdir
from os import path

from qtip.base.constant import BaseProp
from qtip.base.error import NotFoundError
from qtip.loader.base import BaseLoader


ROOT_DIR = path.join(path.dirname(__file__), path.pardir, path.pardir,
                     'resources')


class FileLoader(BaseLoader):
    RELATIVE_PATH = '.'
    _paths = [ROOT_DIR]

    def __init__(self, name, paths=None):
        self._filename = name
        self.abspath = self.find(name, paths=paths)

    @classmethod
    def find(cls, name, paths=None):
        """find a specification in searching paths"""
        paths = cls._paths if paths is None else paths
        for p in paths:
            abspath = path.join(p, cls.RELATIVE_PATH, name)
            if path.exists(abspath):
                return abspath
        raise NotFoundError(name, paths)

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
                BaseProp.ABSPATH: item.abspath}
