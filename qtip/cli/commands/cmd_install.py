##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click


class Install:

    def __init__(self):
        pass

    def list(self):
        click.echo("List all the QTIP release versions.")

    def download(self, version):
        click.echo("Downloading QTIP release version: " + str(version))


@click.group()
def cli():
    pass

_install = Install()


@cli.command('install')
@click.option('--list', is_flag=True, help='List all the available QTIP Versions.')
@click.argument('version', required=False)
def tasks(version, list):
    if list:
        _install.list()
    else:
        _install.download(version)
