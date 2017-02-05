##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from qtip.collector.base import load_parser
from qtip.collector.base import BaseCollector
from qtip.collector.base import CollectorProp as CProp


class LogfileCollector(BaseCollector):
    """collect performance metrics from log files"""
    TYPE = 'logfile'
    LOGS = 'logs'
    PATHS = 'paths'

    def __init__(self, config, parent=None):
        super(LogfileCollector, self).__init__(config)
        self._parent = parent

    def collect(self):
        captured = {}
        for item in self._config[self.LOGS]:
            # TODO(yujunz) resolve key conflict
            captured.update(self._parse_log(item))
        return captured

    @staticmethod
    def _parse_log(log_item):
        group = {}
        for parser_config in log_item[CProp.PARSERS]:
            """
            filename: doctor_consumer.log
            parsers:
              - type: grep
                regex: 'doctor consumer notified at \d+(\.\d+)?$'
                group: notified consumer
            """
            parser = load_parser(parser_config[LogfileCollector.TYPE])(parser_config)
            group.update(parser.run())

        return group
