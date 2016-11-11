##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click


class Uninstall:

    def __init__(self):
        pass

    def delete(self, version, force):
        if force:
            click.echo("Force delete version: " + str(version))
        else:
            click.echo("Deleting version: " + str(version))


@click.group()
def cli():
    pass


_uninstall = Uninstall()


@cli.command('uninstall', help="Uninstall a QTIP version.")
@click.option('-f', '--force', help="Force uninstall", is_flag=True)
@click.argument('version')
def remove(version, force):
    _uninstall.delete(version, force)
