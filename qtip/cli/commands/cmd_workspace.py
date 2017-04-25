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


@click.group()
def cli():
    """ Manage QTIP workspace """
    pass


@cli.command("create", help="Create QTIP workspace")
def create():
    os.system("ANSIBLE_ROLES_PATH={root}/{roles} ansible-playbook "
              "{qtip}/{work_path}/qtip-workspace/create.yml --extra-vars 'qtip_package={qtip_package}'"
              "".format(root=utils.QTIP_PACKAGE, roles=utils.ROLES_PATH, qtip=utils.QTIP_PACKAGE,
                        work_path=utils.ROLES_PATH, qtip_package=utils.QTIP_PACKAGE))
