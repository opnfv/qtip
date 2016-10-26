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
        self.folder = os.path.dirname(__file__)
        self.path = os.path.join(self.folder, '/benchmarks/suite/')

    def list(self):
        table = PrettyTable()
        table.field_names = ["Suite"]
        group = os.listdir(self.path)
        for filename in group:
            table.add_row([filename])
        print(table)

    def run(self):
        print("Run a suite")


@click.group()
def package():
    pass


@package.group()
@click.pass_context
def suite(ctx):
    pass

_suite = Suite()


@suite.command("list", help="Enlists all the suites.")
def enlist():
    _suite.list()


@suite.command("run", help="Executes a single benchmark.")
def execute():
    print("Run")
