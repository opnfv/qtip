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
@click.option('--pod', default='unknown', help='Name of pod under test')
@click.option('--installer', help='OPNFV installer', required=True)
@click.option('--master-host', help='Installer hostname', required=True)
@click.option('--scenario', default='unknown', help='OPNFV scenario')
@click.argument('name')
def create(pod, installer, master_host, scenario, name):
    extra_vars = {
        'qtip_package': utils.QTIP_PACKAGE,
        'cwd': os.getcwd(),
        'pod_name': pod,
        'installer': installer,
        'scenario': scenario,
        'installer_master_host': master_host,
        'workspace': name
    }
    os.system("ANSIBLE_ROLES_PATH={qtip_package}/{roles_path} ansible-playbook"
              " -i {qtip_package}/{roles_path}/qtip-workspace/hosts"
              " {qtip_package}/{roles_path}/qtip-workspace/create.yml"
              " --extra-vars '{extra_vars}'"
              "".format(qtip_package=utils.QTIP_PACKAGE,
                        roles_path=utils.ROLES_PATH,
                        extra_vars=utils.join_vars(**extra_vars)))
