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


class YamlFileLoader(FileLoader):
    """load content from yaml file"""

    def __init__(self, name, paths=None):
        super(YamlFileLoader, self).__init__(name, paths)
        content = defaultdict(lambda: None)

        try:
            content.update(yaml.safe_load(open(self.abspath)))
        except yaml.YAMLError:
            # TODO(yujunz) log yaml error
            raise InvalidFormat(self.abspath)

        self.name = content[BaseProp.NAME] or path.splitext(name)[0]
        self.content = content
