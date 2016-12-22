##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click
from prettytable import PrettyTable
import sys

from qtip.runner.perftest import PerfTest


@click.group()
def cli():
    pass


@cli.group()
def perftest():
    pass


@perftest.command('list', help='List all the PerfTests')
def list():
    perftests = PerfTest.list_all()
    table = PrettyTable(["PerfTest"])
    table.align = 'l'
    for perftest in perftests:
        if perftest['name'].endswith('.yaml'):
            table.add_row([perftest['name']])
    click.echo(table)


@perftest.command('describe', help='Description of PerfTest')
@click.argument('name')
def describe(name):
    perftest = PerfTest(name)
    desc = perftest.describe()
    if desc['abspath'] is None:
        click.echo("Wrong PerfTest specified")
        sys.exit(1)
    else:
        table = PrettyTable(["Name", "Description"])
        table.align = 'l'
        table.add_row([desc['name'], desc['description']])
        click.echo(table)
