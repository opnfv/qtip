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


class Suite:

    def __init__(self):
        self.path = os.path.join(os.environ['PWD'], 'benchmarks/suite/')

    def list(self):
        table = PrettyTable()
        table.field_names = ["Suite"]
        group = os.listdir(self.path)
        for filename in group:
            table.add_row([filename])
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


@suite.command("list", help="Enlists all the different suites.")
def enlist():
    _suite.list()


@suite.command("run", help="Execute one complete suite.")
def execute():
    _suite.run()
