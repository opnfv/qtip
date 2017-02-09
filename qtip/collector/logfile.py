##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from base import BaseCollector

from qtip.collector.base import CollectorProp as CProp
from qtip.loader.file import FileLoader


class LogfileCollector(BaseCollector):
    """collect performance metrics from log files"""

    TYPE = 'logfile'

    def __init__(self, config, parent=None):
        super(LogfileCollector, self).__init__(config)
        paths = [config[CProp.PATHS]] if CProp.PATHS in config else ['.']
        self.loader = FileLoader('.', paths)
        self._parent = parent

    def collect(self):
        captured = {}
        for item in self._config[CProp.LOGS]:
            captured.update(self._parse_log(item))
        return captured

    def _parse_log(self, log_item):
        captured = {}
        # TODO(yujunz) select parser by name
        if CProp.GREP in log_item:
            for rule in log_item[CProp.GREP]:
                captured.update(self._grep(log_item[CProp.FILENAME], rule))
        return captured

    def _grep(self, filename, rule):
        return {}
