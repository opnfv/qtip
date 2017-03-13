##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import click

from qtip.cli import utils
from qtip.cli.entry import Context
from qtip.loader.qpi import QPISpec

pass_context = click.make_pass_decorator(Context, ensure=False)


@click.group()
@pass_context
def cli(ctx):
    ''' Collection of performance tests '''
    pass


@cli.command('list', help='List all the QPI specs')
@pass_context
def cmd_list(ctx):
    qpis = QPISpec.list_all()
    table = utils.table('QPIs', qpis)
    click.echo(table)


@cli.command('show', help='View details of a QPI')
@click.argument('name')
@pass_context
def show(ctx, name):
    qpi = QPISpec('{}.yaml'.format(name))
    cnt = qpi.content
    output = utils.render('qpi', cnt)
    click.echo(output)


@cli.command('run', help='Run performance tests for the specified QPI')
@click.argument('name')
@pass_context
def run(ctx, name):
    pass
