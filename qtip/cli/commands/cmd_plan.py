##############################################################################
# Copyright (c) 2016 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import click
import util

from qtip.cli.entry import Context
from qtip.loader.plan import Plan


pass_context = click.make_pass_decorator(Context, ensure=False)


@click.group()
@pass_context
def cli(ctx):
    ''' Bechmarking Plan '''
    pass


@cli.command('init', help='Initialize Environment')
@pass_context
def init(ctx):
    pass


@cli.command('list', help='List the Plans')
@pass_context
def list(ctx):
    plans = Plan.list_all(paths=[ctx.paths()])
    table = util.table('Plans', plans)
    click.echo(table)


@cli.command('show', help='View details of a Plan')
@click.argument('name')
@pass_context
def show(ctx, name):
    pass


@cli.command('run', help='Execute a Plan')
@click.argument('name')
@pass_context
def run(ctx, name):
    pass
