##############################################################################
# Copyright (c) 2015 Dell Inc  and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import sys
import click
import args_handler


@click.command()
@click.option('--benchmark')
@click.argument('lab', required=True)
@click.argument('suite', required=True)
def Cli(lab, suite, benchmark):

    if not args_handler.check_suit_in_test_list(suite):
        click.echo("\n\n ERROR: Test suite does not exist in test_list/ please enter correct file \n\n")
        sys.exit(0)

    if not args_handler.check_lab_name(lab):
        click.echo("\n\n ERROR: You have specified a lab that is not present in test_cases/ Please enter "
                   "correct file. If unsure how to proceed, use the default lab. \n\n")
        sys.exit(0)

    benchmarks = args_handler.get_files_in_test_list(suite)
    test_cases = args_handler.get_files_in_test_case(lab, suite)
    benchmarks_list = filter(lambda x: x in test_cases, benchmarks)

    if benchmark:
        if not args_handler.check_benchmark_name(lab, suite, benchmark):
            click.echo("\n\n You have specified an incorrect benchmark. Please enter the correct one \n\n")
            sys.exit(0)
        else:
            click.echo("Starting with %s" % benchmark)
            args_handler.prepare_and_run_benchmark(os.environ['INSTALLER_TYPE'], os.environ['INSTALLER_IP'],
                                                   args_handler.get_benchmark_path(lab, suite, benchmark))

    else:
        map(lambda x: args_handler.prepare_and_run_benchmark(
            os.environ['INSTALLER_TYPE'], os.environ['PWD'],
            args_handler.get_benchmark_path(lab, suite, x)), benchmarks_list)

    print('{0} is not a Template in the Directory Enter a Valid file name.'
          'Or use qtip.py -h for list'.format(filter(lambda x: x not in test_cases, benchmarks)))
