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

from qtip.spec.metric import MetricSpec


@click.group()
def cli():
    pass


@cli.group()
def metric():
    pass


@metric.command("list", help="Lists all the Metrics")
def list():
    metrics = MetricSpec.list_all()
    table = PrettyTable(["Name"])
    table.align = 'l'
    for metric in metrics:
        if metric['abspath'].endswith('.yaml'):
            table.add_row([metric['name']])
    click.echo(table)


@metric.command("show", help="Show details of the specified Metric")
@click.argument("name")
def show(name):
    metric = MetricSpec(name)
    results = metric.content()
    table = PrettyTable(["Name", "Description"])
    table.align = 'l'
    table.add_row([results['name'], results['description']])
    click.echo(table)
