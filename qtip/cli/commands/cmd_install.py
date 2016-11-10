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
        click.echo("Downloading QTIP version: " + str(version))


@click.group()
def cli():
    pass


@cli.group()
@click.pass_context
def install(ctx):
    pass

_install = Install()


@install.group()
@click.pass_context
def version(ctx):
    pass


@version.command('list', help="Lists the QTIP release versions.")
def show():
    _install.list()


@version.command('download', help="Download the specified QTIP version.")
@click.option('--tag')
def pull(tag):
    if tag:
        _install.download(tag)
    else:
        _install.download('latest')
