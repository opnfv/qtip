##############################################################################
# Copyright (c) 2015 Dell Inc  and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import sys
import os
from func.env_setup import Env_setup
from func.driver import Driver
from func.spawn_vm import SpawnVM
import argparse


class cli():
    
    def _getfile(self, filepath):
        with open('test_list/'+filepath,'r') as finput:
            _benchmarks=finput.readlines()
        for items in range( len(_benchmarks)):
            _benchmarks[items]=_benchmarks[items].rstrip()
        return _benchmarks
    def _getsuite(self, filepath):
        for suites in range (len(filepath)):
            xindex= filepath[suites].find('.')
            filepath[suites]=filepath[suites][0:xindex]
        return filepath
        
    def __init__(self):
        suite=[]
        parser = argparse.ArgumentParser()
        parser.add_argument('-l ', '--lab', help='Name of Lab on which being tested ')
        parser.add_argument('-f', '--file', help = 'File in test_list with the list ' \
                                                'of tests')
        args = parser.parse_args()
        benchmarks = self._getfile(args.file)
        suite.append(args.file)
        suite=self._getsuite(suite)
        for items in range (len(benchmarks)):
            if (suite and benchmarks):

                roles=''
                vm_info=''
                benchmark_details=''
                pip=''
                obj=''
                obj = Env_setup()
                if os.path.isfile('./test_cases/'+args.lab.lower()+'/'+suite[0]+'/' +benchmarks[items]):
                    [benchmark, roles, vm_info, benchmark_details, pip] = obj.parse('./test_cases/'
                                                                    +args.lab.lower()+'/'+suite[0]+'/'+benchmarks[items])
                    
                    if len(vm_info) != 0:
                        vmObj =''
                        vmObj = SpawnVM(vm_info)
                    obj.callpingtest()
                    obj.callsshtest()
                    obj.updateAnsible()
                    dvr = Driver()
                    dvr.drive_bench(benchmark, obj.roles_dict.items(), benchmark_details, obj.ip_pw_dict.items())
                else:
                    print (args.benchmark, ' is not a Template in the Directory - \
                                Enter a Valid file name. or use qtip.py -h for list')
        