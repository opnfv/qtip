#############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click

from qtip.cli.entry import pass_context

# TODO(Taseer) implementation


@click.group()
@pass_context
def cli(ctx):
    ''' Bechmarking Plan '''
    # ctx.verbose('Verbose mode on')


@cli.command('list', help='List the Plans')
@pass_context
def list(ctx):
    pass


@cli.command('run', help='Execute a Plan')
@click.argument('name')
@pass_context
def run(name, ctx):
    pass


@cli.command('show', help='View details of Plan')
@click.argument('name')
@pass_context
def show(name, ctx):
    pass
