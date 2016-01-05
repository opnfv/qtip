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
        self.dic_json = defaultdict()

    def drive_bench(self, benchmark, roles, benchmark_detail= None, pip_dict = None):
        roles= sorted(roles)
        pip_dict = sorted(pip_dict)
        result_dir = 'results'
        benchmark_name = benchmark + '.yaml'
        self.dic_json['Dest_dir'] = str(result_dir)
        self.dic_json['ip1']=''
        self.dic_json['ip2']=''

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
                        self.dic_json['privateip'+str(index)] = pip_dict[0][1]
                        index= index+1
            dic_json = json.dumps(dict(self.dic_json.items()))
            print dic_json
            run_play = 'ansible-playbook -s ./benchmarks/playbooks/{0} --private-key=./data/QtipKey -i ./data/hosts --extra-vars \'{1}\' -v '.format(benchmark_name, dic_json)
#            run_play = 'ansible-playbook -s $PWD/benchmarks/playbooks/{0} --extra-vars "Dest_dir={1} role={2}" -vvv'.format(
#            benchmark_name, result_dir, k)
            status = os.system(run_play)

