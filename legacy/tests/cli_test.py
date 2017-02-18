##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import pytest
import mock
import os
from qtip.utils.cli import Cli
from os.path import expanduser


@pytest.mark.skip("TODO(yujunz) recover test after refactoring")
class TestClass:
    @pytest.mark.parametrize("test_input, expected", [
        (['-l',
          'zte',
          '-f',
          'compute'], "You have specified a lab that is not present under benchmarks/testplan"),
        (['-l',
          'default',
          '-f',
          'test'], "This suite file test doesn't exist under benchmarks/suite/")
    ])
    def test_cli_error(self, capfd, test_input, expected):
        k = mock.patch.dict(os.environ, {'INSTALLER_TYPE': 'fuel', 'PWD': '/home'})
        with pytest.raises(SystemExit):
            k.start()
            Cli(test_input)
            k.stop()
        with open(expanduser('~') + "/qtip/logs/cli.log", "r") as file:
            data = file.read()
        assert expected in data

    @pytest.mark.parametrize("test_input, expected", [
        (['-l',
          'default',
          '-f',
          'storage'], [('fuel', '/home', 'benchmarks/testplan/default/storage/fio_bm.yaml'),
                       ('fuel', '/home', 'benchmarks/testplan/default/storage/fio_vm.yaml')])
    ])
    @mock.patch('qtip.utils.cli.args_handler.prepare_and_run_benchmark')
    def test_cli_successful(self, mock_args_handler, test_input, expected):
        k = mock.patch.dict(os.environ, {'INSTALLER_TYPE': 'fuel', 'PWD': '/home'})
        k.start()
        Cli(test_input)
        k.stop()
        call_list = map(lambda x: mock_args_handler.call_args_list[x][0], range(len(expected)))
        assert sorted(call_list) == sorted(expected)
