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
from operator import add

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
            logger.info("Setup test enviroment, Done!")

    def cleanup(self):
        self.env.cleanup()

    def run(self, metric_list, **kwargs):
        if 'args' in self.config:
            extra_vars = self.merge_two_dicts(kwargs, self.config['args'])
        else:
            extra_vars = kwargs
        logger.info("extra_var: {0}".format(extra_vars))

        tool_to_metrics = defaultdict(list)
        for metric in metric_list:
            if metric == 'dhrystone' or metric == 'whetstone':
                tool_to_metrics['unixbench'].append(metric)
                extra_vars[metric] = True
            elif metric == 'ssl':
                tool_to_metrics['openssl'].append(metric)
            else:
                tool_to_metrics[metric].append(metric)

        result_list = map(lambda tool: self._run_metric(tool,
                                                        tool_to_metrics[tool],
                                                        extra_vars),
                          tool_to_metrics)
        return False not in result_list

    def _run_metric(self, tool, metrics, extra_vars):
        logger.info('Using {0} to measure metrics {1}'.format(tool, metrics))

        setup_pbook = "{0}/{1}/setup.yaml".format(PLAYBOOK_DIR, tool)
        run_pbook = "{0}/{1}/run.yaml".format(PLAYBOOK_DIR, tool)
        clean_pbook = "{0}/{1}/clean.yaml".format(PLAYBOOK_DIR, tool)

        if self._run_ansible_playbook(setup_pbook, extra_vars):
            self._run_ansible_playbook(run_pbook, extra_vars)
        else:
            logger.error("{0} is failed.".format(setup_pbook))

        return self._run_ansible_playbook(clean_pbook, extra_vars)

    def _run_ansible_playbook(self, pbook, extra_vars):
        ansible_api = AnsibleApi()
        logger.debug("Run {0} with extra_vars: {1}".format(pbook, extra_vars))
        ansible_api.execute_playbook(pbook, self.env.hostfile,
                                     self.env.keypair['private'], extra_vars)
        playbook_stats = ansible_api.get_detail_playbook_stats()
        logger.debug("playbook_stat: {0}".format(playbook_stats))
        return self.is_pass(playbook_stats)

    @staticmethod
    def is_pass(stats):
        return 0 == reduce(add,
                           map(lambda x: x[1]['failures'] + x[1]['unreachable'],
                               stats))
