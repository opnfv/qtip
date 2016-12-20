##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import pytest
import mock
import qtip.utils.args_handler

@pytest.mark.xfail
class TestClass:
    @pytest.mark.parametrize("test_input, expected", [
        (['fuel', '/home', 'benchmarks/testplan/default/network/iperf_bm.yaml'],
         ['fuel', '/home', "iperf",
          [('1-server', ['10.20.0.23']), ('2-host', ['10.20.0.24'])],
          "iperf_bm.yaml",
          [('duration', 20), ('protocol', 'tcp'), ('bandwidthGbps', 10)],
          [("10.20.0.24", [None]), ("10.20.0.23", [None])], {}])
    ])
    @mock.patch('qtip.utils.args_handler.Env_setup.call_ping_test')
    @mock.patch('qtip.utils.args_handler.Env_setup.call_ssh_test')
    @mock.patch('qtip.utils.args_handler.Env_setup.update_ansible')
    @mock.patch('qtip.utils.args_handler.SpawnVM')
    @mock.patch('qtip.utils.args_handler.Driver.drive_bench')
    def test_prepare_and_run_benchmark_successful(self, mock_driver, mock_sqawn_vm, mock_env_setup_ping,
                                                  mock_env_setup_ssh, mock_update_ansible, test_input, expected):
        mock_ips = mock.Mock(return_value=["10.20.0.23", "10.20.0.24"])
        qtip.utils.args_handler.Env_setup.fetch_compute_ips = mock_ips
        qtip.utils.args_handler.prepare_and_run_benchmark(test_input[0], test_input[1], test_input[2])
        call = mock_driver.call_args
        call_args, call_kwargs = call
        assert sorted(map(sorted, call_args)) == sorted(map(sorted, expected))
