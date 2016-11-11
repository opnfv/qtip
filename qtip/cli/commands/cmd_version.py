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

    def show_version(self):
        click.echo("Returns the currently installed version")


@click.group()
def cli():
    pass

_version = Version()


@cli.command('version')
def curr_ver():
    _version.show_version()
