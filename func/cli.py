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
import args_handler
import argparse


class cli:

    @staticmethod
    def _parse_args(args):
        parser = argparse.ArgumentParser()
        parser.add_argument('-l ', '--lab', required=True, help='Name of Lab '
                            'on which being tested, These can'
                            'be found in the test_cases/ directory. Please '
                            'ensure that you have edited the respective files '
                            'before using them. For testing other than through Jenkins'
                            ' The user should list default after -l . all the fields in'
                            ' the files are necessary and should be filled')
        parser.add_argument('-f', '--file', required=True, help='File in '
                            'test_list with the list of tests. there are three files'
                            '\n compute '
                            '\n storage '
                            '\n network '
                            'They contain all the tests that will be run. They are listed by suite.'
                            'Please ensure there are no empty lines')
        return parser.parse_args(args)

    def __init__(self, args=sys.argv[1:]):

        args = self._parse_args(args)
        if not args_handler.check_suit_in_test_list(args.file):
            print('\n\n ERROR: Test File Does not exist in test_list/ please enter correct file \n\n')
            sys.exit(0)

        if not args_handler.check_lab_name(args.lab):
            print('\n\n You have specified a lab that is not present in test_cases/ please enter \
                   correct file. If unsure how to proceed, use -l default.\n\n')
            sys.exit(0)
        suite = args.file
        benchmarks = args_handler.get_files_in_test_list(suite)
        test_cases = args_handler.get_files_in_test_case(args.lab, suite)
        benchmarks_list = filter(lambda x: x in test_cases, benchmarks)

        map(lambda x: args_handler.prepare_and_run_benchmark(
            os.environ['INSTALLER_TYPE'], os.environ['PWD'],
            args_handler.get_benchmark_path(args.lab.lower(), suite, x)), benchmarks_list)

        print('{0} is not a Template in the Directory Enter a Valid file name.'
              'or use qtip.py -h for list'.format(filter(lambda x: x not in test_cases, benchmarks)))
