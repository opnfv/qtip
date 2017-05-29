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
@click.option('--pod', default='unknown', help='Name of pod under test')
@click.option('--installer', help='OPNFV installer', default='manual')
@click.option('--master-host', help='Installer hostname', default='dummy-host')
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


@cli.command(context_settings=CONTEXT_SETTINGS, help='Setup testing environment')
@click.pass_context
def setup(ctx):
    project.setup(" ".join(ctx.args))


@cli.command(context_settings=CONTEXT_SETTINGS, help='Execute testing plan')
@click.pass_context
def run(ctx):
    project.run(" ".join(ctx.args))


@cli.command(context_settings=CONTEXT_SETTINGS, help='Teardown testing environment')
@click.pass_context
def teardown(ctx):
    project.teardown(ctx.args)
