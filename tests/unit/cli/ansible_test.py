##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from click.testing import CliRunner
from qtip.cli.entry import cli


class TestClass(object):

    @pytest.fixture()
    def runner(self):
        return CliRunner()

    def test_prepare(self, runner):
        result = runner.invoke(cli, ['ansible', 'prepare'])
        assert result.output == ""

    def test_show(self, runner):
        result = runner.invoke(cli, ['ansible', 'show'])
        assert result.output == ""

    def test_status(self, runner):
        result = runner.invoke(cli, ['ansible', 'status'])
        assert result.output == ""
