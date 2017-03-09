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
import pickle

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
    types = ['report', 'sys_info', 'timeline']
    reporter = ConsoleReporter({})
    conf_path = path.join(path.dirname(__file__), os.pardir, os.pardir, os.pardir,
                          'tests/data/reporter/dicts/')

    for i in range(0, len(types)):
        var_dict = pickle.load(open('{}{}{}'.format(conf_path, types[i], '.pickle'), 'rb'))
        out = reporter.render(var_dict, types[i])
        pickle.dump(out, open('{}{}'.format(types[i], '.pickle'), 'wb'))
        click.echo(out)
