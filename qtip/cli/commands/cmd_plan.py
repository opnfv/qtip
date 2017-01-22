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

from qtip.loader.plan import Plan
from qtip.cli.entry import pass_context


@click.group()
@pass_context
def cli(ctx):
    ''' Bechmarking Plan '''
    pass


@cli.command('init', help='Initialize Environment')
@click.option('--inst_type', prompt='Installer Type')
@click.option('--inst_ip', prompt='Installer IP')
@click.option('--ext_net', prompt='Openstack External Network')
@pass_context
def init(ctx, inst_type, inst_ip, ext_net):
    pass


@cli.command('list', help='List the Plans')
@pass_context
def list(ctx):
    pass


@cli.command('run', help='Execute a Plan')
@click.argument('name')
@pass_context
def run(ctx, name):
    pass
