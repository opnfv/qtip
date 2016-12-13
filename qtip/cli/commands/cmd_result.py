##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click


class Result:

    def __init__(self):
        pass

    def list(self):
        click.echo("List")

    def node(self):
        click.echo("Node names")

    def view(self, name, node):
        click.echo("Showing: %s " % name + " on %s " % node)


@click.group()
def cli():
    pass


@cli.group()
def result():
    pass


_result = Result()


@result.command("list", help="List all PerfTests carried out")
def list():
    _result.list()


@result.command("node", help="List all the compute nodes in cluster")
def node():
    _result.node()


@result.command("view", help="View the result of specified PerfTest")
@click.argument("name")
@click.argument("node")
def view(name, node):
    _result.view(name, node)
