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
from collections import defaultdict

class Driver:

    def __init__(self):

        print "Class driver initialized\n"
        print os.environ['PWD']
        self.dic_json = defaultdict()

    def drive_bench(self, benchmark, roles, benchmark_fname, benchmark_detail = None, pip_dict = None, proxy_info = None):
        roles= sorted(roles)
        pip_dict = sorted(pip_dict)
        result_dir = 'results'
        benchmark_name = benchmark + '.yaml'
        self.dic_json['Dest_dir'] = str(result_dir)
        self.dic_json['ip1'] = ''
        self.dic_json['ip2'] = ''
        self.dic_json['installer'] = str(os.environ['INSTALLER_TYPE'])
        self.dic_json['workingdir'] = str(os.environ['PWD'])
        self.dic_json['fname'] = str(benchmark_fname)
        self.dic_json['username'] = str('root')
        
        for key in proxy_info.keys():
            self.dic_json[key] = proxy_info[key]
                    
        if os.environ['INSTALLER_TYPE'] == str('joid'):
            self.dic_json['username']=str('ubuntu')
        if os.environ['INSTALLER_TYPE'] == str('apex'):
            self.dic_json['username']=str('heat-admin')
        for k,v in benchmark_detail:
            self.dic_json[k]=v
        for k, v in roles:
            self.dic_json['role']=k
            index=1
            if benchmark_detail != None:
                for values in v:
                    if k ==  '1-server':
                        print values, 'saving IP'
                        self.dic_json['ip'+str(index)]= str(values)
                        if pip_dict[0][1][0]:
                            self.dic_json['privateip'+str(index)] = pip_dict[0][1]
                        if not pip_dict[0][1][0]:
                           self.dic_json['privateip'+str(index)] = 'NONE'
                        index= index+1
            dic_json = json.dumps(dict(self.dic_json.items()))
            print dic_json
            run_play = 'ansible-playbook ./benchmarks/playbooks/{0}  --private-key=./data/QtipKey -i ./data/hosts --extra-vars \'{1}\''.format(benchmark_name, dic_json)
            status = os.system(run_play)
