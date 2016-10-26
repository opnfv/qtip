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
import json
import click


class Perftest:

    def __init__(self):
        self.folder = os.path.dirname(__file__)
        self.path = os.path.join(self.folder, '/benchmarks/suite/')

    def list(self):
        table = PrettyTable()
        table.field_names = ["Perftest"]
        group = os.listdir(self.path)
        for filename in group:
            with open(self.path + "/" + filename) as result:
                line = result.read()
                bm = json.loads(line)['bm']
                vm = json.loads(line)['vm']
                for points in bm:
                    table.add_row([points])
                for points in vm:
                    table.add_row([points])
        print(table)

    def run(self):
        print("Run a benchmark")


@click.group()
def perf():
    pass


@perf.group()
@click.pass_context
def perftest(ctx):
    pass

_perftest = Perftest()


@perftest.command("list", help="Enlists all the benchmarks.")
def enlist():
    _perftest.list()


@perftest.command("run", help="Executes a single benchmark.")
def execute():
    print("Run")
