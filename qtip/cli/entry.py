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
import pkg_resources as pkg
import sys

from qtip.cli.commands.cmd_project import cli as project_commands

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# TODO (taseer) define user friendly error messages
sys.tracebacklimit = 0


class Context(object):
    """ Load configuration and pass to subcommands """


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))


class SubCommand(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('qtip.cli.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=SubCommand, context_settings=CONTEXT_SETTINGS,
               invoke_without_command=True)
def sub_commands(ctx, verbose, debug):
    pass


@click.command(cls=click.CommandCollection,
               help="Platform performance benchmarking",
               sources=[sub_commands, project_commands],
               invoke_without_command=True)
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose mode.')
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode.')
@click.version_option(pkg.require("qtip")[0])
@pass_context
def cli(ctx, verbose, debug):
    if debug:
        sys.tracebacklimit = 8
