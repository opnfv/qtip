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


roles_path = 'resources/ansible_roles'


@click.group()
def cli():
    """ Manage QTIP workspace """
    pass


@cli.command("create", help="Create QTIP workspace")
def create():
    os.system("ANSIBLE_ROLES_PATH={0}/{1} ansible-playbook "
              "{2}/{3}/qtip-workspace/create.yml --extra-vars 'qtip_package={4}'"
              "".format(utils.qtip_package, roles_path, utils.qtip_package,
                        roles_path, utils.qtip_package))
