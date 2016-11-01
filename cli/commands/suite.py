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


class Suite:

    def __init__(self):
        self.path = 'benchmarks/suite/summary'

    def list(self):
        table = PrettyTable(["Name", "Description"])
        table.align = 'l'
        with open(self.path) as tests:
            line = tests.read()
            data = yaml.safe_load(line)['suite_cases']
            for i in range(0, len(data)):
                points = data[i]
                table.add_row([points['name'], points['description']])
        click.echo(table)

    def run(self):
        print("Run a suite")


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
def execute():
    _suite.run()
