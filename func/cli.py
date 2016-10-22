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
from utils import logger_utils

logger = logger_utils.QtipLogger('cli').get


class Cli:

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
                            'benchmarks/suite/ with the list of tests. there are three files'
                            '\n compute '
                            '\n storage '
                            '\n network '
                            'They contain all the tests that will be run. They are listed by suite.'
                            'Please ensure there are no empty lines')
        parser.add_argument('-b', '--benchmark', help='Name of the benchmark.'
                            'Can be found in benchmarks/suite/file_name')

        return parser.parse_args(args)

    def __init__(self, args=sys.argv[1:]):

        args = self._parse_args(args)
        if not args_handler.check_suite(args.file):
            logger.error("ERROR: This suite file doesn't exist under benchmarks/suite/.\
                Please enter correct file." % str(args.file))
            sys.exit(1)

        if not args_handler.check_lab_name(args.lab):
            logger.error("You have specified a lab that is not present under test_cases/.\
                Please enter correct file. If unsure how to proceed, use -l default.")
            sys.exit(1)
        suite = args.file
        benchmarks = args_handler.get_files_in_suite(suite)
        test_cases = args_handler.get_files_in_test_case(args.lab, suite)
        benchmarks_list = filter(lambda x: x in test_cases, benchmarks)

        if args.benchmark:
            if not args_handler.check_benchmark_name(args.lab, args.file, args.benchmark):
                logger.error("You have specified an incorrect benchmark.\
                    Please enter the correct one.")
                sys.exit(1)
            else:
                logger.info("Starting with " + args.benchmark)
                args_handler.prepare_and_run_benchmark(
                    os.environ['INSTALLER_TYPE'], os.environ['PWD'],
                    args_handler.get_benchmark_path(args.lab.lower(), args.file, args.benchmark))
        else:
            map(lambda x: args_handler.prepare_and_run_benchmark(
                os.environ['INSTALLER_TYPE'], os.environ['PWD'],
                args_handler.get_benchmark_path(args.lab.lower(), suite, x)), benchmarks_list)

        logger.info("{0} is not a Template in the Directory Enter a Valid file name.\
            or use qtip.py -h for list".format(filter(lambda x: x not in test_cases, benchmarks)))
