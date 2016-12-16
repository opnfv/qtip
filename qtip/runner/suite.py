##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from os import path
import yaml

from benchmark import Benchmark, Property
from qtip.utils.logger_utils import QtipLogger

logger = QtipLogger('suite').get


class Suite(Benchmark):
    """WIP(yujunz):
    a suite is consist of one or several perf tests and produces one QPI.
    It must be executed as part of testplan
    """

    # paths to search for suites
    _paths = [path.join(p, 'suite') for p in Benchmark._paths]

    def __init__(self, name):
        self.content = None
        super(self.__class__, self).__init__(name)
        self._load()

    def _load(self):
        self.content = yaml.safe_load(file(self._abspath))
        if not self.content:
            logger.warning("suite %s is empty" % self.name)

    def _get(self, key):
        try:
            return self.content.get(key, None)
        except AttributeError:
            return None

    def describe(self):
        info = super(self.__class__, self).describe()
        info[Property.CONTENT] = self.content
        info[Property.DESCRIPTION] = self._get('description')
        return info
