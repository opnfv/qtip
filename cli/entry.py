##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click

from cli.commands.cli_ansible import CliAnsible
from cli.commands.suite import Suite

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.1.dev0')
def cli():
    pass

_ansible = CliAnsible()


@cli.group()
@click.pass_context
def ansible(ctx):
    pass


@ansible.command('prepare', help="Prepares the ansible environment. "
                                 "This step is needed run benchmarks.")
def ansible_prepare():
    _ansible.prepare()


@ansible.command('show', help="Shows the current ansible configuration.")
def ansible_show():
    _ansible.show()


@ansible.command('status', help="Checks if ansible still connects to hosts.")
def ansible_status():
    _ansible.status()


@cli.group()
@click.pass_context
def suite(ctx):
    pass

_suite = Suite()


@suite.command("list", help="Lists all the available suites")
def list():
    _suite.list()


@suite.command("run", help="Execute one complete suite")
def execute():
    _suite.run()
