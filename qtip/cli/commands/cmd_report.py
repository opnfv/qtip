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
@pass_context
def show(ctx):
    reporter = ConsoleReporter({})
    click.echo(reporter.render('detail.json'))
    click.echo(reporter.render('timeline.json'))
