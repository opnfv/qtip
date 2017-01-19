##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from collections import defaultdict
from os import path
import yaml

from qtip.base.error import InvalidFormat
from qtip.base.constant import BaseProp
from qtip.loader.file import FileLoader

ROOT_DIR = path.join(path.dirname(__file__), path.pardir, path.pardir,
                     'opt')


class YamlFileLoader(FileLoader):
    """Abstract class of QTIP specification loader"""
    RELATIVE_PATH = '.'
    _paths = [ROOT_DIR]

    def __init__(self, name, paths=None):
        super(YamlFileLoader, self).__init__(name, paths)
        content = defaultdict(lambda: None)

        try:
            content.update(yaml.safe_load(file(self._abspath)))
        except yaml.YAMLError:
            # TODO(yujunz) log yaml error
            raise InvalidFormat(self._abspath)

        self.name = content[BaseProp.NAME] or path.splitext(name)[0]
        self.content = content
