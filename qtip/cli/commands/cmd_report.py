##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click
import json
import os

from os import path
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
    result = {}
    types = ['detail', 'timeline']
    reporter = ConsoleReporter({})
    result_path = path.join(path.dirname(__file__), os.pardir, os.pardir, os.pardir,
                            'tests/data/reporter/dicts/')
    for kind in types:
        with open('{}{}{}'.format(result_path, kind, '.json')) as sample:
            result = json.load(sample)
            out = reporter.render(result, kind)
            click.echo(out)
