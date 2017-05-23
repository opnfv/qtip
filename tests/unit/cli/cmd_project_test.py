###############################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os


class TestProject:

    @staticmethod
    def run(cmd):
        os.system(cmd)

    @staticmethod
    def setup(cmd):
        os.system(cmd)

    @staticmethod
    def teardown(cmd):
        os.system(cmd)


def test_run(mocker):
    mocker.patch('os.system')
    TestProject.run('ansible-playbook run.yml -vvv')
    os.system.assert_called_once_with('ansible-playbook run.yml -vvv')


def test_setup(mocker):
    mocker.patch('os.system')
    TestProject.setup('ansible-playbook setup.yml -vvv')
    os.system.assert_called_once_with('ansible-playbook setup.yml -vvv')


def test_teardown(mocker):
    mocker.patch('os.system')
    TestProject.teardown('ansible-playbook teardown.yml -vvv')
    os.system.assert_called_once_with('ansible-playbook teardown.yml -vvv')
