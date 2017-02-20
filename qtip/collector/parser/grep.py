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
from qtip.base import BaseActor


class GrepProp(BaseProp):
    FILENAME = 'filename'
    REGEX = 'regex'


class GrepParser(BaseActor):
    TYPE = 'grep'

    def run(self):
        filename = self._parent.get_config(GrepProp.FILENAME)
        return grep_in_file(self._parent.find(filename), self._config[GrepProp.REGEX])


def grep_in_file(filename, regex):
    with open(filename, "r") as outfile:
        return filter(lambda x: x is not None,
                      list(re.finditer(regex, outfile.read(), re.MULTILINE)))
