##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from prettytable import PrettyTable
import yaml
import click
import os
from cli import helper
from func import args_handler


class PerfTest:

    def __init__(self):
        self.path = os.path.join(helper.fetch_root(), 'perftest/summary')

    def list(self):
        table = PrettyTable(["Name", "Description"])
        table.align = 'l'
        with open(self.path) as tests:
            line = tests.read()
            data = yaml.safe_load(line)['test_cases']
            for i in range(0, len(data)):
                points = data[i]
                table.add_row([points['name'], points['description']])
        click.echo(table)

    def run(self, lab, suite, benchmark):
        if args_handler.check_benchmark_name(lab, suite, benchmark):
            args_handler.prepare_and_run_benchmark(
                os.environ['INSTALLER_TYPE'], os.environ['PWD'],
                args_handler.get_benchmark_path(lab, suite, benchmark))
        else:
            click.echo("Incorrect benhmark name. Please specify the correct one.")


@click.group()
def cli():
    pass


@cli.group()
@click.pass_context
def perftest(ctx):
    pass

_perftest = PerfTest()


@perftest.command("list", help="Lists all perftest benchmarks.")
def list():
    _perftest.list()


@perftest.command("run", help="Execute a single perftest benchmark")
@click.argument("lab")
@click.argument("suite")
@click.argument("benchmark")
def execute(lab, suite, benchmark):
    _perftest.run(lab, suite, benchmark)
