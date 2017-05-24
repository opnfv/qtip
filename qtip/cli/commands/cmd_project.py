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
from qtip.runner import project


class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


@click.command(cls=AliasedGroup, help="Project commands")
def cli():
    pass


@cli.command(help="Create new testing project")
@click.option('--template',
              prompt='Choose project template',
              type=click.Choice(['compute', 'doctor']),
              default='compute',
              help='Choose project template')
@click.option('--pod', default='unknown', prompt='Pod Name',
              help='Name of pod under test')
@click.option('--installer', prompt='OPNFV Installer',
              help='OPNFV installer', default='manual')
@click.option('--master-host', prompt='Installer Hostname',
              help='Installer hostname', default='dummy-host')
@click.option('--scenario', prompt='OPNFV Scenario', default='unknown',
              help='OPNFV scenario')
@click.argument('name')
def create(pod, installer, master_host, scenario, name, template):
    qtip_generator_role = os.path.join(utils.QTIP_ANSIBLE_ROLES, 'qtip-generator')
    extra_vars = {
        'qtip_package': utils.QTIP_PACKAGE,
        'cwd': os.getcwd(),
        'pod_name': pod,
        'installer': installer,
        'scenario': scenario,
        'installer_master_host': master_host,
        'project_name': name,
        'project_template': template
    }
    os.system("ANSIBLE_ROLES_PATH={roles_path} ansible-playbook"
              " -i {hosts}"
              " {playbook}"
              " --extra-vars '{extra_vars}'"
              "".format(roles_path=utils.QTIP_ANSIBLE_ROLES,
                        hosts=os.path.join(qtip_generator_role, 'hosts'),
                        playbook=os.path.join(qtip_generator_role, 'main.yml'),
                        extra_vars=utils.join_vars(**extra_vars)))


@cli.command(help='Setup testing environment')
def setup():
    project.setup()


@cli.command(help='Execute testing plan')
def run():
    project.run()


@cli.command(help='Teardown testing environment')
def teardown():
    project.teardown()
