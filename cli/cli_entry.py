##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click

from cli.commands.cli_perftest import CliPerftest
from cli.commands.cli_suite import CliSuite


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='opnfv qtip.0.1 ')
def cli():
    pass


@cli.group()
@click.pass_context
def suite(ctx):
    pass

_suite = CliSuite()


@suite.command('list', help="Lists the different suites. ")
def list_suite():
    _suite.list()


@suite.command('run', help='Executes one complete suite from the list. '
               'Use list to view the differet suites.')
def run_suite():
    _suite.run()


@cli.group()
@click.pass_context
def perftest(ctx):
    pass

_perftest = CliPerftest()


@perftest.command('list', help="Lists the different suites. ")
def list_perftest():
    _perftest.list()


@perftest.command('run', help='Executes one benchmark. Use list to view '
                  'complete set of benchmarks.')
def run_perftest():
    _perftest.run()
