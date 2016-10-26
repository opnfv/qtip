##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click
from commands import perftest
from commands import suite

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

cli = click.CommandCollection(sources=[perftest.perf, suite.package])

if __name__ == '__main__':
    cli()
