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
from qtip.loader.metric import MetricSpec


@click.group()
def cli():
    ''' Performance Metrics Group '''
    pass


@cli.command('list', help='List all the Metric Groups')
def cmd_list():
    metrics = MetricSpec.list_all()
    table = utils.table('Metrics', metrics)
    click.echo(table)


@cli.command('show', help='View details of a Metric')
@click.argument('name')
def show(name):
    try:
        metric = MetricSpec('{}.yaml'.format(name))
    except NotFoundError as nf:
        click.echo(Fore.RED + "ERROR: metric spec: " + nf.message)
    except InvalidContentError as ice:
        click.echo(Fore.RED + "ERROR: metric spec " + ice.message)
    else:
        cnt = metric.content
        output = utils.render('metric', cnt)
        click.echo(output)


@cli.command('run', help='Run performance test')
@click.argument('name')
@click.option('-p', '--path', help='Path to store results')
def run(name, path):
    runner_path = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir,
                               'runner/runner.py')
    os.system('python {0} -b {1} -d {2}'.format(runner_path, name, path))
