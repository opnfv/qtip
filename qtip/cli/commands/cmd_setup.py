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


@click.command('setup', help='Setup QTIP workspace')
@click.argument('workspace')
def cli(workspace):
    os.system('ansible-playbook {}/qtip-workspace/'
              '{}/setup.yml'.format(utils.roles_path, workspace))
