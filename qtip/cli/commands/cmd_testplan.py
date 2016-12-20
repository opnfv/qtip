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
from qtip.runner.plan import TestPlan


@click.group()
def cli():
    pass


@cli.group()
def testplan():
    pass


@testplan.command('list', help='List the different TestPlans.')
def list():
    testplans = TestPlan.list_all()
    table = PrettyTable(["Testplans"])
    table.align = 'l'
    for testplan in testplans:
        table.add_row([testplan['name']])
    click.echo(table)


@testplan.command('show', help='Show details of specified TestPlan.')
@click.argument('name')
def show(name):
    plan = TestPlan(name)
    results = plan.content()
    table = PrettyTable(["Name", "Description"])
    table.align = 'l'
    table.add_row([results['name'], results['description']])
    click.echo(table)
