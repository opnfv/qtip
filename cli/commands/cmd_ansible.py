##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os

import click

ANSIBLE_CONF = '{}/conf/ansible.cfg'.format(os.environ['HOME'])


class Ansible:

    def __init__(self):
        pass

    def show(self):
        click.echo("show ansible configuration")
        pass

    def prepare(self):
        click.echo("prepare ansible env")
        pass

    def status(self):
        click.echo("check connectivity")
        pass


_ansible = Ansible()


@click.group()
@click.pass_context
def cli():
    pass


@cli.command('prepare', help="Prepares the ansible environment. "
                                 "This step is needed run benchmarks.")
def ansible_prepare():
    _ansible.prepare()


@cli.command('show', help="Shows the current ansible configuration.")
def ansible_show():
    _ansible.show()


@cli.command('status', help="Checks if ansible still connects to hosts.")
def ansible_status():
    _ansible.status()
