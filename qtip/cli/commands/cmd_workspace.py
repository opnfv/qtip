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
from os import path


roles_path = path.join(path.dirname(__file__), os.pardir, os.pardir, os.pardir,
                       "resources/ansible_roles")
playbook_path = path.join(path.dirname(__file__), os.pardir, os.pardir, os.pardir,
                          "tests/integration")


@click.group()
def cli():
    """ Manage QTIP workspace """
    pass


@cli.command("create", help="Create QTIP workspace")
def create():
    os.system("ANSIBLE_ROLES_PATH={0} ansible_playbook"
              "{1}/workspace-create.yml".format(roles_path, playbook_path))
