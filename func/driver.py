##############################################################################
# Copyright (c) 2015 Dell Inc, ZTE  and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from utils import logger_utils
from ansible_api import AnsibleApi

logger = logger_utils.QtipLogger('driver').get


class Driver:

    def __init__(self):

        logger.info("Class driver initialized\n")
        self.installer_username = {'fuel': 'root',
                                   'joid': 'ubuntu',
                                   'apex': 'heat-admin'}

    @staticmethod
    def merge_two_dicts(x, y):
        '''
        It is from http://stackoverflow.com/questions/38987/
        how-can-i-merge-two-python-dictionaries-in-a-single-expression
        '''
        z = x.copy()
        z.update(y)
        return z

    def get_common_var_json(self, installer_type, pwd, benchmark_fname,
                            benchmark_detail, pip_dict, proxy_info):
        common_json = {'Dest_dir': 'results',
                       'ip1': '',
                       'ip2': '',
                       'installer': str(installer_type),
                       'workingdir': str(pwd),
                       'fname': str(benchmark_fname),
                       'username': self.installer_username[str(installer_type)]}
        common_json.update(benchmark_detail) if benchmark_detail else None
        common_json.update(proxy_info) if proxy_info else None
        return common_json

    def get_special_var_json(self, role, roles, benchmark_detail, pip_dict):
        special_json = {}
        index = roles.index(role) + 1
        private_ip = pip_dict[0][1][0] if pip_dict[0][1][0] else 'NONE'
        map(lambda x: special_json.update({'ip' + str(index): x}), role[1])\
            if benchmark_detail and (role[0] == '1-server') else None
        map(lambda x: special_json.update({'privateip' + str(index): private_ip}), role[1])\
            if benchmark_detail and (role[0] == '1-server') else None
        special_json = self.get_special_var_json(filter(lambda x: x[0] == '1-server', roles)[0],
                                                 roles,
                                                 benchmark_detail,
                                                 pip_dict) if role[0] == '2-host' else special_json
        special_json.update({'role': role[0]})
        return special_json

    def run_ansible_playbook(self, benchmark, extra_vars):
        logger.info(extra_vars)
        ansible_api = AnsibleApi()
        ansible_api.execute_playbook('./data/hosts',
                                     './benchmarks/playbooks/{0}.yaml'.format(benchmark),
                                     './data/QtipKey', extra_vars)
        return ansible_api.get_detail_playbook_stats()

    def drive_bench(self, installer_type, pwd, benchmark, roles, benchmark_fname,
                    benchmark_detail=None, pip_dict=None, proxy_info=None):
        roles = sorted(roles)
        pip_dict = sorted(pip_dict)
        var_json = self.get_common_var_json(installer_type, pwd, benchmark_fname,
                                            benchmark_detail, pip_dict, proxy_info)
        map(lambda role: self.run_ansible_playbook
            (benchmark, self.merge_two_dicts(var_json,
                                             self.get_special_var_json(role, roles,
                                                                       benchmark_detail,
                                                                       pip_dict))), roles)
