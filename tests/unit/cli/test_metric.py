###############################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest
from click.testing import CliRunner

from qtip.cli.commands.cmd_metric import cli


class TestClass(object):

    @pytest.fixture()
    def runner(self):
        return CliRunner()

    def test_list(self, runner):
        result = runner.invoke(cli, ['list'])
        assert '' in result.output

    def test_run(self, runner):
        result = runner.invoke(cli, ['run'])
        assert '' in result.output
