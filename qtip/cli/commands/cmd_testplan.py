#############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click

from qtip.runner.testplan import TestPlan


@click.group()
def cli():
    pass


@cli.group()
def testplan():
    pass


# _testplan = TestPlan('compute')


@testplan.command('list', help='List the different tesplans.')
def list():
    pass


@testplan.command('show', help='Show details of specified plan.')
@click.argument('testplan_name')
def show(testplan_name):
    pass
