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
import handler


class PerfTest:

    def __init__(self):
        self.path = os.path.join(handler.fetch_root(), 'perftest/summary')

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

    def run(self):
        click.echo("Run a perftest")


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


@perftest.command("run", help="Executes a single perftest benchmark.")
def execute():
    _perftest.run()
