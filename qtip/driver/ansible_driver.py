##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from os import path

from qtip.driver.ansible_api import AnsibleApi
from qtip.util.env import AnsibleEnvSetup

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
            print("Already setup environment......")
        else:
            print("Starting to setup test environment...")
            self.env.setup(self.config)
            self.env_setup_flag = True
            print("Done!")

    def run(self, metric_list, **kwargs):
        if 'args' in self.config:
            extra_vars = self.merge_two_dicts(kwargs, self.config['args'])
        else:
            extra_vars = kwargs

        ansible_api = AnsibleApi()
        map(lambda metric: self._run_metric(ansible_api, metric, extra_vars),
            metric_list)

    def _run_metric(self, ansible_api, metric, extra_vars):
        header = 'Starting to run metric: {0}'.format(metric)
        print('#' * 80)
        print('#{:78}#'.format(header))
        print('#' * 80)
        for item in ('setup', 'run', 'clean'):
            pbook = "{0}/{1}/{2}.yaml".format(PLAYBOOK_DIR, metric, item)
            ansible_api.execute_playbook(pbook, self.env.hostfile,
                                         self.env.keypair['private'], extra_vars)
            ansible_api.get_detail_playbook_stats()
        print('#' * 80)
