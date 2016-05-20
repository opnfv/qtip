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

        return filepath

    def _checkTestList(self, filename):

        if os.path.isfile('test_list/'+filename):
            return True
        else:
            return False

    def _checkLabName(self, labname):

        if os.path.isdir('test_cases/'+labname):
            return True
        else:
            return False

    def _get_fname(self,file_name):

        return file_name[0: file_name.find('.')]

    def __init__(self):

        suite=[]
        parser = argparse.ArgumentParser()
        parser.add_argument('-l ', '--lab', help='Name of Lab on which being tested, These can' \
                                            'be found in the test_cases/ directory. Please ' \
                                            'ensure that you have edited the respective files '\
                                            'before using them. For testing other than through Jenkins'\
                                            ' The user should list default after -l . all the fields in'\
                                            ' the files are necessary and should be filled')
        parser.add_argument('-f', '--file', help = 'File in test_list with the list of tests. there are three files' \
                                            '\n compute '\
                                            '\n storage '\
                                            '\n network '\
                                            'They contain all the tests that will be run. They are listed by suite.' \
                                            'Please ensure there are no empty lines')
        args = parser.parse_args()

        if not self._checkTestList(args.file):
            print '\n\n ERROR: Test File Does not exist in test_list/ please enter correct file \n\n'
            sys.exit(0)

        if not self._checkLabName(args.lab):
            print '\n\n You have specified a lab that is not present in test_cases/ please enter correct'\
                    ' file. If unsure how to proceed, use -l default.\n\n'
            sys.exit(0)

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
                    [benchmark, roles, vm_info, benchmark_details, pip, proxy_info] = obj.parse('./test_cases/'
                                                                    +args.lab.lower()+'/'+suite[0]+'/'+benchmarks[items])

                    if len(vm_info) != 0:
                        vmObj =''
                        vmObj = SpawnVM(vm_info)
                    obj.callpingtest()
                    obj.callsshtest()
                    obj.updateAnsible()
                    dvr = Driver()
                    dvr.drive_bench(benchmark,
                                    obj.roles_dict.items(),
                                    self._get_fname(benchmarks[items]),
                                    benchmark_details,
                                    obj.ip_pw_dict.items(),
                                    proxy_info)
                else:
                    print (args.benchmark, ' is not a Template in the Directory - \
                                Enter a Valid file name. or use qtip.py -h for list')
