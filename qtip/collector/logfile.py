##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import re

from base import BaseCollector
from qtip.base.constant import CollectorProp as CProp
from qtip.loader.file import FileLoader


class LogfileCollector(BaseCollector):
    """collect performance metrics from log files"""

    def __init__(self, config, paths=None):
        super(LogfileCollector, self).__init__(config)
        if 'paths' in self._config:
            self.paths = self._config[CProp.PATHS]
        else:
            self.paths = paths
        self.loader = FileLoader('.', paths)

    def collect(self):
        captured = {}
        for item in self._config[CProp.LOGS]:
            print "item:%s" % item
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


class SysLogfileCollector(LogfileCollector):

    def __init__(self, config, paths=None):
        super(SysLogfileCollector, self).__init__(config, paths)

    def _parse_log(self, log_item):
        captured = {}
        if log_item['filename'] == 'inxi.log':
            with open(self.paths + '/inxi.log', 'r') as origin_inxi:
                with open(self.paths + '/inxi_new.log', 'w+') as new_inxi:
                    new_inxi.write(origin_inxi.read().replace('\n', ''))
            log_item['filename'] = 'inxi_new.log'

        if CProp.SHELL in log_item:
            for s_item in log_item['shell']:
                captured.update(self._shell(log_item[CProp.FILENAME], s_item))

        if "cpu_idle" in captured:
            captured.update({
                "cpu_usage": self._calculate_cpu_usage(captured['cpu_idle'])
            })
            captured.pop("cpu_idle")

        if "network" in captured:
            captured.update(self._reorganize_network(captured['network']))
            captured.pop('network')

        return captured

    def _shell(self, filename, rule):
        try:
            cmd = """cat {0}/{1} | {2} """.format(self.paths, filename, rule['cmd'])
            return {rule['capture']: os.popen(cmd).read().strip()}
        except Exception, e:
            print(e)
            return {}

    @staticmethod
    def _calculate_cpu_usage(cpu_idle):
        cpu_usage = round((100.0 - float(cpu_idle)), 3)
        return '{0}%'.format(str(cpu_usage))

    @staticmethod
    def _reorganize_network(network):
        network_interface = {}
        network_list = re.split("\s{2,10}", network)
        for i in range(0, len(network_list) - 1, 2):
            interface_info = network_list[i + 1]
            interface_name = \
                re.findall('IF:\s\w+', interface_info)[0].split(':')[-1].strip()
            network_interface[interface_name] = {}
            interface_info_list = re.findall('\w+:\s\w+\s', interface_info)
            for info in interface_info_list:
                key_value = info.split(":")
                key = key_value[0].strip()
                if key == 'speed':
                    value = key_value[1].strip() + 'Mbps'
                else:
                    value = key_value[1].strip()
                if key != 'IF':
                    network_interface[interface_name][key] = value
            network_interface[interface_name]['network_card'] = \
                network_list[i].split('driver:')[0].split(':')[-1].strip()
        return network_interface
