##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import click


@click.group()
def cli():
    ''' Collection of performance tests '''
    pass


@cli.command('list', help='List all the QPI specs')
def cmd_list():
    pass


@cli.command('show', help='View details of a QPI')
@click.argument('name')
def show(name):
    pass
