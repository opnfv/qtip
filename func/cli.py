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


class cli:

    @staticmethod
    def _getfile(file_path):
        with open('test_list/' + file_path, 'r') as fin_put:
            _benchmarks = fin_put.readlines()
        for items in range(len(_benchmarks)):
            _benchmarks[items] = _benchmarks[items].rstrip()
        return _benchmarks

    @staticmethod
    def _getsuite(file_path):

        return file_path

    @staticmethod
    def _check_test_list(filename):

        if os.path.isfile('test_list/' + filename):
            return True
        else:
            return False

    @staticmethod
    def _check_lab_name(lab_name):

        if os.path.isdir('test_cases/' + lab_name):
            return True
        else:
            return False

    @staticmethod
    def _get_f_name(file_name):

        return file_name[0: file_name.find('.')]

    @staticmethod
    def _parse_args(args):
        parser = argparse.ArgumentParser()
        parser.add_argument('-l ', '--lab', required=True, help='Name of Lab on which being tested, These can'
                            'be found in the test_cases/ directory. Please '
                            'ensure that you have edited the respective files '
                            'before using them. For testing other than through Jenkins'
                            ' The user should list default after -l . all the fields in'
                            ' the files are necessary and should be filled')
        parser.add_argument('-f', '--file', required=True, help='File in test_list with the list of tests. there are three files'
                            '\n compute '
                            '\n storage '
                            '\n network '
                            'They contain all the tests that will be run. They are listed by suite.'
                            'Please ensure there are no empty lines')
        return parser.parse_args(args)

    def __init__(self, args=sys.argv[1:]):

        suite = []
        args = self._parse_args(args)

        if not self._check_test_list(args.file):
            print '\n\n ERROR: Test File Does not exist in test_list/ please enter correct file \n\n'
            sys.exit(0)

        if not self._check_lab_name(args.lab):
            print '\n\n You have specified a lab that is not present in test_cases/ please enter correct \
                   file. If unsure how to proceed, use -l default.\n\n'
            sys.exit(0)

        benchmarks = self._getfile(args.file)
        suite.append(args.file)
        suite = self._getsuite(suite)
        for items in range(len(benchmarks)):
            if suite and benchmarks:
                obj = Env_setup()
                if os.path.isfile('./test_cases/' + args.lab.lower() + '/' + suite[0] + '/' + benchmarks[items]):
                    [benchmark, vm_info, benchmark_details, proxy_info] = \
                        obj.parse('./test_cases/' + args.lab.lower() + '/' + suite[0] + '/' + benchmarks[items])

                    if len(vm_info) != 0:
                        SpawnVM(vm_info)
                    obj.call_ping_test()
                    obj.call_ssh_test()
                    obj.update_ansible()
                    dvr = Driver()
                    dvr.drive_bench(benchmark,
                                    obj.roles_dict.items(),
                                    self._get_f_name(benchmarks[items]),
                                    benchmark_details,
                                    obj.ip_pw_dict.items(),
                                    proxy_info)
                else:
                    print (benchmarks[items], ' is not a Template in the Directory - \
                                Enter a Valid file name. or use qtip.py -h for list')
