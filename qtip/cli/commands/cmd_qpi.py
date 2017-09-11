##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import click
import os
from os import path
from prettytable import PrettyTable
import yaml

QPI_PATH = path.join(path.dirname(__file__), '..', '..', '..',
                     'resources', 'QPI')


@click.group()
def cli():
    """ Collection of performance tests """
    pass


@cli.command('list', help='List all the QPI specs')
def cmd_list():
    table = PrettyTable(['QPI', 'Description'])
    table.align = 'l'
    for qpi in os.listdir(QPI_PATH):
        if qpi.endswith('yaml'):
            with open('{}/{}'.format(QPI_PATH, qpi)) as conf:
                details = yaml.safe_load(conf)
            table.add_row([details['name'], details['description']])
    click.echo(table)


@cli.command('show', help='View details of a QPI')
@click.argument('name')
def show(name):
    table = PrettyTable(['QPI', 'Description', 'Formula'])
    table.align = 'l'
    with open('{}/{}.yaml'.format(QPI_PATH, name)) as conf:
        qpi = yaml.safe_load(conf)
    for section in qpi['sections']:
        try:
            table.add_row([section['name'], section['description'],
                           section['formula']])
        except Exception:
            table.add_row([section['name'], section['description'],
                           'Not Available'])
    click.echo(table)
