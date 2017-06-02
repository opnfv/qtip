###############################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest
import re
import sys

from click.testing import CliRunner
from qtip.cli.entry import cli


class TestClass(object):

    @pytest.fixture()
    def runner(self):
        return CliRunner()

    def test_version(self, runner):
        result = runner.invoke(cli, ['--version'])
        assert re.search(r'\d+\.\d+\.\d+', result.output)

    def test_debug(self, runner):
        runner.invoke(cli, ['-d'])
        assert sys.tracebacklimit == 8
