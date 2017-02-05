##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import re


from qtip.base.constant import BaseProp
from qtip.collector.parser.base import BaseParser


class GrepProp(BaseProp):
    FILENAME = 'filename'
    REGEX = 'regex'
    GROUP = 'group'


class GrepParser(BaseParser):
    TYPE = 'grep'

    def run(self):
        config = self._config
        return self.search(config[GrepProp.FILENAME], GrepProp.REGEX, GrepProp.GROUP)

    @staticmethod
    def search(filename, regex, group_name=GrepProp.GROUP):
        # TODO(yujunz) extend to multiple groups
        with open(filename) as f:
            for line in f:
                match = re.search(regex, line)
                if match:
                    return {group_name: match.group(1)}
