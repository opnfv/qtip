##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import click
from colorama import Fore
import os

from qtip.base.error import InvalidContentError
from qtip.base.error import NotFoundError
from qtip.cli import utils
from qtip.loader.qpi import QPISpec


@click.group()
def cli():
    ''' Collection of performance tests '''
    pass


@cli.command('list', help='List all the QPI specs')
def cmd_list():
    qpis = QPISpec.list_all()
    table = utils.table('QPIs', qpis)
    click.echo(table)


@cli.command('show', help='View details of a QPI')
@click.argument('name')
def show(name):
    try:
        qpi = QPISpec('{}.yaml'.format(name))
    except NotFoundError as nf:
        click.echo(Fore.RED + "ERROR: qpi spec: " + nf.message)
    except InvalidContentError as ice:
        click.echo(Fore.RED + "ERROR: qpi spec: " + ice.message)
    else:
        cnt = qpi.content
        output = utils.render('qpi', cnt)
        click.echo(output)


@cli.command('run', help='Run performance tests for the specified QPI')
@click.argument('name')
@click.option('-p', '--path', help='Path to store results')
def run(name, path):
    runner_path = path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir,
                            'runner/runner.py')
    os.system('python {0} -b all -d {1}'.format(runner_path, path))
