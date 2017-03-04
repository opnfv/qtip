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

from qtip.driver.ansible_api import AnsibleApi
from qtip.util.env import AnsibleEnvSetup
from qtip.util.logger import QtipLogger

logger = QtipLogger('ansible_driver').get
PLAYBOOK_DIR = path.join(path.dirname(__file__), 'playbook')


class AnsibleDriver(object):
    """driver for running performance tests with Ansible"""

    def __init__(self, config={}):
        self.config = config
        self.env = AnsibleEnvSetup()
        self.env_setup_flag = False

    @staticmethod
    def merge_two_dicts(x, y):
        '''
        It is from http://stackoverflow.com/questions/38987/
        how-can-i-merge-two-python-dictionaries-in-a-single-expression
        '''
        z = x.copy()
        z.update(y)
        return z

    def pre_run(self):
        if self.env_setup_flag:
            logger.info("Already setup environment......")
        else:
            logger.info("Starting to setup test environment...")
            self.env.setup(self.config)
            self.env_setup_flag = True
            logger("Done!")

    def run(self, metric_list, **kwargs):
        if 'args' in self.config:
            extra_vars = self.merge_two_dicts(kwargs, self.config['args'])
        else:
            extra_vars = kwargs
        logger.info("extra_var: {0}".format(extra_vars))

        # TODO zhihui: will add a new property named "tool" for metrics, hardcode it now.
        tool_to_metrics = defaultdict(list)
        for metric in metric_list:
            if metric in ['dhrystone', 'whetstone']:
                tool_to_metrics['unixbench'].append(metric)
                extra_vars[metric] = True
            else:
                tool_to_metrics[metric].append(metric)

        ansible_api = AnsibleApi()
        map(lambda tool: self._run_metric(ansible_api, tool,
                                          tool_to_metrics[tool], extra_vars),
            tool_to_metrics)

    def _run_metric(self, ansible_api, tool, metrics, extra_vars):
        logger.info('Using {0} to measure metrics {1}'.format(tool, metrics))

        for metric in metrics:
            extra_vars[metric] = True

        logger.debug("extra_vars: {0}".format(extra_vars))

        for item in ['setup', 'run', 'clean']:
            pbook = "{0}/{1}/{2}.yaml".format(PLAYBOOK_DIR, tool, item)
            logger.debug("Start to run {0}".format(pbook))
            ansible_api.execute_playbook(pbook, self.env.hostfile,
                                         self.env.keypair['private'], extra_vars)
            playbook_stat = ansible_api.get_detail_playbook_stats()
            logger.debug("playbook_stat: {0}".format(playbook_stat))
