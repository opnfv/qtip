##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
import os
import re
import yaml

from os import path
from qtip.base.constant import CollectorProp as CProp

CONF_DIR = path.join(path.dirname(__file__), 'conf')


class SysInfo(object):

    def __init__(self):
        self.log_path = None
        self.sysinfo = {}
        self._config = yaml.safe_load(file(CONF_DIR + '/sysinfo.yaml'))

    def parser_sysinfo(self, log_path, result_path=""):
        self.log_path = log_path
        if not result_path:
            result_path = log_path
        self._parser_log()
        self._calculate_cpu_usage()
        self._reorganize_network()
        print(self.sysinfo)
        with open(result_path + '/sysinfo.json', 'w+') as result_json:
            json.dump(self.sysinfo, result_json, indent=4, sort_keys=True)

    def _calculate_cpu_usage(self):
        try:
            cpu_usage = round((100.0 - float(self.sysinfo['cpu_idle'])), 3)
            self.sysinfo['cpu_usage'] = '{0}%'.format(str(cpu_usage))
            self.sysinfo.pop('cpu_idle', None)
        except KeyError:
            print("Not get the value of cpu_idle {0}, "
                  "can't calculate cpu usage".format(self.sysinfo['cpu_idle']))

    def _reorganize_network(self):
        self.sysinfo['network_interface'] = {}
        network_list = re.split("\s{2,10}", self.sysinfo['network'])
        for i in range(0, len(network_list) - 1, 2):
            interface_info = network_list[i + 1]
            interface_name = \
                re.findall('IF:\s\w+', interface_info)[0].split(':')[-1].strip()
            self.sysinfo['network_interface'][interface_name] = {}
            interface_info_list = re.findall('\w+:\s\w+\s', interface_info)
            for info in interface_info_list:
                key_value = info.split(":")
                key = key_value[0].strip()
                if key == 'speed':
                    value = key_value[1].strip() + 'Mbps'
                else:
                    value = key_value[1].strip()
                if key != 'IF':
                    self.sysinfo['network_interface'][interface_name][key] = value
            self.sysinfo['network_interface'][interface_name]['network_card'] = \
                network_list[i].split('driver:')[0].split(':')[-1].strip()
        self.sysinfo.pop('network', None)

    def _parser_log(self):
        for item in self._config:
            if not path.isfile(self.log_path + '/' + item['filename']):
                print("{0} doesn't exist under "
                      "{1}".format(item['filename'], self.log_path))
                continue

            if item['filename'] == 'inxi.log':
                with open(self.log_path + '/inxi.log', 'r') as origin_inxi:
                    with open(self.log_path + '/inxi_new.log', 'w+') as new_inxi:
                        new_inxi.write(origin_inxi.read().replace('\n', ''))
                item['filename'] = 'inxi_new.log'

            if CProp.SHELL in item:
                for s_item in item['shell']:
                    self.sysinfo[s_item['capture'].lower()] = \
                        self._shell(item['filename'], s_item['cmd'])

    def _shell(self, filename, rule):
        try:
            cmd = """cat {0}/{1} | {2} """.format(self.log_path, filename, rule)
            return os.popen(cmd).read().strip()
        except Exception, e:
            print(e)
            return None
