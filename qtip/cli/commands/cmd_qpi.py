##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import click

from qtip.cli.entry import Context

pass_context = click.make_pass_decorator(Context, ensure=False)


@click.group()
@pass_context
def cli(ctx):
    ''' Collection of performance tests '''
    pass


@cli.command('list', help='List all the QPI specs')
@pass_context
def cmd_list(ctx):
    pass


@cli.command('show', help='View details of a QPI')
@click.argument('name')
@pass_context
def show(ctx, name):
    pass


@cli.command('run', help='Run performance tests for the specified QPI')
@click.argument('name')
@pass_context
def run(ctx, name):
    pass
