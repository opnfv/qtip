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


class CliAnsible:

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
