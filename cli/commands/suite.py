##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from prettytable import PrettyTable
import os
import click
from func import args_handler


class Suite:

    def __init__(self):
        self.path = os.path.join(args_handler.fetch_root(), 'suite/')

    def list(self):
        table = PrettyTable(["Name"])
        table.align = 'l'
        suites = os.listdir(self.path)
        for suite in suites:
            table.add_row([suite])
        click.echo(table)

    def run(self, lab, suite_case):
        if args_handler.check_suite(suite_case):
            benchmarks = args_handler.get_files_in_suite(suite_case)
            test_cases = args_handler.get_files_in_test_case(lab, suite_case)
            benchmarks_list = filter(lambda x: x in test_cases, benchmarks)

            map(lambda x: args_handler.prepare_and_run_benchmark(
                os.environ['INSTALLER_TYPE'], os.environ['PWD'],
                args_handler.get_benchmark_path(lab, suite_case, x)), benchmarks_list)
        else:
            click.echo("Incorrect suite specified.")


@click.group()
def cli():
    pass


@cli.group()
@click.pass_context
def suite(ctx):
    pass

_suite = Suite()


@suite.command("list", help="Lists all the available suites")
def list():
    _suite.list()


@suite.command("run", help="Execute one complete suite")
@click.argument("lab")
@click.argument("suite_case")
def execute(lab, suite_case):
    _suite.run(lab, suite_case)
