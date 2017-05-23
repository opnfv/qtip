###############################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from click.testing import CliRunner
import os
import pytest

from qtip.cli.entry import cli


@pytest.fixture(scope='module')
def runner():
    return CliRunner()


def test_run(mocker, runner):
    mocker.patch('os.system')
    runner.invoke(cli, ['run', '-vvv'])
    os.system.assert_called_once_with('ansible-playbook run.yml -vvv')


def test_setup(mocker, runner):
    mocker.patch('os.system')
    runner.invoke(cli, ['setup', '-vvv'])
    os.system.assert_called_once_with('ansible-playbook setup.yml -vvv')


def test_teardown(mocker, runner):
    mocker.patch('os.system')
    runner.invoke(cli, ['teardown', '-vvv'])
    os.system.assert_called_once_with('ansible-playbook teardown.yml -vvv')
