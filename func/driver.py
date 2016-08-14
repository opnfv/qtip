##############################################################################
# Copyright (c) 2015 Dell Inc  and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import json


class Driver:

    def __init__(self):

        print "Class driver initialized\n"
        print os.environ['PWD']
        self.installer_username = {'fuel': 'root',
                                   'joid': 'ubuntu',
                                   'apex': 'heat-admin'}

    @staticmethod
    def merge_two_dicts(x, y):
        z = x.copy()
        z.update(y)
        return z

    def get_common_var_json(self, benchmark_fname, benchmark_detail, pip_dict, proxy_info):
        dic_json = {'Dest_dir': 'results',
                    'ip1': '',
                    'ip2': '',
                    'installer': str(os.environ['INSTALLER_TYPE']),
                    'workingdir': str(os.environ['PWD']),
                    'fname': str(benchmark_fname),
                    'username': self.installer_username[str(os.environ['INSTALLER_TYPE'])]}
        dic_json.update(benchmark_detail) if benchmark_detail else None
        dic_json.update(proxy_info) if proxy_info else None
        return dic_json

    def get_special_var_json(self, role, roles, benchmark_detail, pip_dict):
        special_json = {}
        index = roles.index(role) + 1
        special_json.update({'role': role[0]})
        private_ip = pip_dict[0][1] if pip_dict[0][1][0] else 'NONE'
        map(lambda x: special_json.update({'ip' + str(index): x}), role[1])\
            if benchmark_detail and (role[0] == '1-server') else None
        map(lambda x: special_json.update({'privateip' + str(index): private_ip}), role[1])\
            if benchmark_detail and (role[0] == '1-server') else None
        return special_json

    def run_ansible_playbook(self, benchmark, extra_vars):
        dic_json = json.dumps(dict(extra_vars.items()))
        print dic_json
        run_play = 'ansible-playbook ./benchmarks/playbooks/{0}.yaml  --private-key=./data/QtipKey -i ./data/hosts --extra-vars \'{1}\''.format(benchmark, dic_json)
        os.system(run_play)

    def drive_bench(self, benchmark, roles, benchmark_fname, benchmark_detail=None, pip_dict=None, proxy_info=None):
        roles = sorted(roles)
        pip_dict = sorted(pip_dict)
        var_json = self.get_common_var_json(benchmark_fname, benchmark_detail, pip_dict, proxy_info)
        map(lambda role: self.run_ansible_playbook
            (benchmark, self.merge_two_dicts(var_json,
                                             self.get_special_var_json(role, roles,
                                                                       benchmark_detail,
                                                                       pip_dict))), roles)
