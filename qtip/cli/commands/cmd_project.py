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


CONTEXT_SETTINGS = dict(ignore_unknown_options=True, allow_extra_args=True, )


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
@click.argument('project_name')
@click.option('--project-template',
              # TODO(yujunz) create template list by directory name
              type=click.Choice(['compute', 'doctor', 'storage']),
              default='compute',
              help='Choose project template')
@click.option('--pod-name',
              prompt='Pod Name',
              default='opnfv-pod',
              help='Name of pod under test')
@click.option('--installer-type',
              type=click.Choice(['apex', 'fuel', 'manual', 'mcp']),
              prompt='OPNFV Installer Type',
              default='manual',
              help='OPNFV installer')
@click.option('--installer-host',
              prompt='Installer SSH Host Address',
              help='Host configured for ssh client or IP addresses and domain name')
@click.option('--scenario',
              help='OPNFV scenario')
@click.option('--sut',
              prompt='System Under Test type',
              help='Type of system can be vnf')
def create(project_name,
           project_template,
           pod_name,
           installer_type,
           installer_host,
           scenario,
           sut):
    qtip_generator_role = os.path.join(utils.QTIP_ANSIBLE_ROLES, 'qtip-generator')
    extra_vars = {
        'qtip_package': utils.QTIP_PACKAGE,
        'cwd': os.getcwd(),
        'project_name': project_name,
        'project_template': project_template,
        'pod_name': pod_name,
        'installer_type': installer_type,
        'installer_host': installer_host,
        'scenario': scenario,
        'sut': sut
    }
    os.system("ANSIBLE_ROLES_PATH={roles_path} ansible-playbook"
              " -i {hosts}"
              " {playbook}"
              " --extra-vars '{extra_vars}'"
              "".format(roles_path=utils.QTIP_ANSIBLE_ROLES,
                        hosts=os.path.join(qtip_generator_role, 'hosts'),
                        playbook=os.path.join(qtip_generator_role, 'main.yml'),
                        extra_vars=utils.join_vars(**extra_vars)))


@cli.command(context_settings=CONTEXT_SETTINGS, help='Setup testing environment')
@click.pass_context
def setup(ctx):
    project.setup(ctx.args)


@cli.command(context_settings=CONTEXT_SETTINGS, help='Execute testing plan')
@click.pass_context
def run(ctx):
    project.run(ctx.args)


@cli.command(context_settings=CONTEXT_SETTINGS, help='Teardown testing environment')
@click.pass_context
def teardown(ctx):
    project.teardown(ctx.args)
