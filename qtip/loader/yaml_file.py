##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from os import path
import yaml

from qtip.base.error import InvalidContentError
from qtip.base.constant import BaseProp
from qtip.loader.file import FileLoader


class YamlFileLoader(FileLoader):
    """load content from yaml file"""

    def __init__(self, name, paths=None):
        super(YamlFileLoader, self).__init__(name, paths)
        abspath = self.abspath

        with open(abspath, 'r') as stream:
            content = yaml.safe_load(stream)
            if not isinstance(content, dict):
                raise InvalidContentError(abspath)
            self.content = content
            self.name = content.get(BaseProp.NAME, path.splitext(name)[0])
