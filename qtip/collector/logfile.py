##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from itertools import chain
from six.moves import reduce
import os

from qtip.base import BaseActor
from qtip.collector import load_parser
from qtip.collector import CollectorProp as CProp
from qtip.loader.file import FileLoader


class LogItem(BaseActor):
    def find(self, filename, paths=None):
        return self._parent.find(filename, paths)


class LogfileCollector(BaseActor):
    """run performance metrics from log files"""
    TYPE = 'logfile'
    LOGS = 'logs'
    PATHS = 'paths'

    def __init__(self, config, parent=None):
        super(LogfileCollector, self).__init__(config)
        self._parent = parent  # plan
        dirname = os.path.dirname(self._parent.abspath)
        paths = [os.path.join(dirname, p) for p in config.get(self.PATHS, [])]
        self._loader = FileLoader('.', paths)

    def run(self):
        collected = []
        for log_item_config in self._config[self.LOGS]:
            log_item = LogItem(log_item_config, self)
            matches = reduce(chain, [load_parser(c[CProp.TYPE])(c, log_item).run()
                                     for c in log_item.get_config(CProp.PARSERS)])
            collected = chain(collected, matches)
        return collected

    def find(self, filename, paths=None):
        return self._loader.find(filename, paths)
