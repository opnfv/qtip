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

from qtip.runner.metric import Metric


@click.group()
def cli():
    pass


@cli.group()
def metric():
    pass


@metric.command('list', help='List all the Metrics')
def list():
    metrics = Metric.list_all()
    table = PrettyTable(["Metric"])
    table.align = 'l'
    for metric in metrics:
        if metric['name'].endswith('.yaml'):
            table.add_row([metric['name']])
    click.echo(table)


@metric.command('describe', help='Description of Metric')
@click.argument('name')
def describe(name):
    metric = Metric(name)
    desc = metric.describe()
    if desc['abspath'] is None:
        click.echo("Wrong PerfTest specified")
        sys.exit(1)
    else:
        table = PrettyTable(["Name", "Description"])
        table.align = 'l'
        table.add_row([desc['name'], desc['description']])
        click.echo(table)
