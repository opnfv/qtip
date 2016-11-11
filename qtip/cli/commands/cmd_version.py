##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click


class Version:

    def __init__(self):
        pass

    def list(self):
        click.echo("Lists all the different versions")

    def install(self, number):
        click.echo("Install: %s" % number)

    def uninstall(self, number):
        click.echo("Uninstall: %s" % number)


@click.group()
def cli():
    pass


@cli.group()
def version():
    pass

_version = Version()


@version.command('list', help="List all the available QTIP versions.")
def show():
    _version.list()


@version.command('install', help="Install the specified QTIP version.")
@click.argument('number')
def download(number):
    _version.install(number)


@version.command('uninstall', help="Install the specified QTIP version.")
@click.argument('number')
def remove(number):
    _version.uninstall(number)
