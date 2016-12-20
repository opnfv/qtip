#############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click
from prettytable import PrettyTable
from qtip.runner.plan import Plan


@click.group()
def cli():
    pass


@cli.group()
def plan_cmd():
    pass


@plan_cmd.command('list', help='List the different TestPlans.')
def list_all():
    plans = Plan.list_all()
    table = PrettyTable(["Testplans"])
    table.align = 'l'
    for plan in plans:
        table.add_row([plan['name']])
    click.echo(table)


@plan_cmd.command('show', help='Show details of specified TestPlan.')
@click.argument('name')
def show(name):
    plan = Plan(name)
    results = plan.content()
    table = PrettyTable(["Name", "Description"])
    table.align = 'l'
    table.add_row([results['name'], results['description']])
    click.echo(table)
