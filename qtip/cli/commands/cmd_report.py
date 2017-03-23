##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click

from qtip.cli.entry import Context
from qtip.reporter.console import ConsoleReporter

pass_context = click.make_pass_decorator(Context, ensure=False)


@click.group()
@pass_context
def cli(ctx):
    """ View Qtip results"""
    pass


@cli.command('show')
@click.argument('metric')
@click.option('-p', '--path', help='Path to result directory')
@pass_context
def show(ctx, metric, path):
    reporter = ConsoleReporter({})
    report = reporter.render(metric, path)
    click.echo(report)
