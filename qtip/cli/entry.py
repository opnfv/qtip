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
import sys

from qtip.cli.commands.cmd_project import cli as project_commands


sys.tracebacklimit = 0
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


@click.command(cls=SubCommand,
               invoke_without_command=True)
def sub_commands(debug):
    pass


@click.command(cls=click.CommandCollection,
               help="Platform performance benchmarking",
               sources=[sub_commands, project_commands],
               invoke_without_command=True)
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode.')
@click.version_option()
def cli(debug):
    if debug:
        sys.tracebacklimit = 8
