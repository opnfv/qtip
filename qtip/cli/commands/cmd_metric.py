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

from qtip.cli import utils
from qtip.cli.entry import Context
from qtip.loader.metric import MetricSpec

pass_context = click.make_pass_decorator(Context, ensure=False)


@click.group()
@pass_context
def cli(ctx):
    ''' Performance Metrics Group '''
    pass


@cli.command('list', help='List all the Metric Groups')
@pass_context
def cmd_list(ctx):
    metrics = MetricSpec.list_all()
    table = utils.table('Metrics', metrics)
    click.echo(table)


@cli.command('show', help='View details of a Metric')
@click.argument('name')
@pass_context
def show(ctx, name):
    metric = MetricSpec('{}.yaml'.format(name))
    cnt = metric.content
    output = utils.render('metric', cnt)
    click.echo(output)


@cli.command('run', help='Run performance test')
@click.argument('name')
@click.option('-p', '--path', help='Path to store results')
@pass_context
def run(ctx, name, path):
    runner_path = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir,
                               'runner/runner.py')
    os.system('python {0} -b {1} -d {2}'.format(runner_path, name, path))
