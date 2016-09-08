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
import func.args_handler


class TestClass:
    @pytest.mark.parametrize("test_input, expected", [
        ('./test_cases/zte-pod1/network/iperf_bm.yaml',
         ["iperf",
          [('1-server', ['10.20.0.23']), ('2-host', ['10.20.0.24'])],
          "iperf_bm.yaml",
          [('duration', 20), ('protocol', 'tcp'), ('bandwidthGbps', 10)],
          [("10.20.0.24", [None]), ("10.20.0.23", [None])], {}])
    ])
    @mock.patch('func.args_handler.Baremetal.call_ping_test')
    @mock.patch('func.args_handler.Baremetal.call_ssh_test')
    @mock.patch('func.args_handler.Baremetal.update_ansible')
    @mock.patch('func.args_handler.Virtual')
    @mock.patch('func.args_handler.Driver.drive_bench')
    def test_prepare_and_run_benchmark_successful(self, mock_driver, mock_virtual, mock_env_setup_ping,
                                                  mock_env_setup_ssh, mock_update_ansible, test_input, expected):
        mock_ips = mock.Mock(return_value=["10.20.0.23", "10.20.0.24"])
        func.args_handler.Baremetal.fetch_compute_ips = mock_ips
        func.args_handler.prepare_and_run_benchmark(test_input)
        call = mock_driver.call_args
        call_args, call_kwargs = call
        assert sorted(map(sorted, call_args)) == sorted(map(sorted, expected))

    def test_setup_test_env_bm_successful(self):
        test_case = './test_cases/default/compute/dhrystone_bm.yaml'
        func.args_handler.Baremetal.__init__ = mock.Mock(return_value=None)
        env = func.args_handler.setup_test_env(test_case)
        assert(isinstance(env, func.args_handler.Baremetal))

    def test_setup_test_env_vm_successful(self):
        test_case = './test_cases/default/compute/dhrystone_vm.yaml'
        func.args_handler.Virtual.__init__ = mock.Mock(return_value=None)
        env = func.args_handler.setup_test_env(test_case)
        assert(isinstance(env, func.args_handler.Virtual))

    def test_setup_test_env_failed(self):
        test_case = './tests/test_case/error.yaml'
        func.args_handler.Baremetal.__init__ = mock.Mock(return_value=None)
        with pytest.raises(KeyError) as excinfo:
            func.args_handler.setup_test_env(test_case)
        expect = "Keyword Virtual_Machines or Host_Machines is None in %s" % test_case
        assert excinfo.value.message == expect

    def test_prepare_ansible_env_successful(self):
        test_case = './test_cases/default/network/iperf_bm.yaml'
        mock_ips = mock.Mock(return_value=["10.20.0.23", "10.20.0.24"])
        func.args_handler.Baremetal.fetch_compute_ips = mock_ips
        func.args_handler.Baremetal.setup = mock.Mock()
        mock_args = mock.Mock(return_value=['iperf', {}, {}])
        func.args_handler.Baremetal.handler_args = mock_args
        func.args_handler.Baremetal.call_ping_test = mock.Mock()
        func.args_handler.Baremetal.call_ssh_test = mock.Mock()
        func.args_handler.Baremetal.update_ansible = mock.Mock()
        benchmark, benchmark_details, proxy_info, env = \
            func.args_handler.prepare_ansible_env(test_case)
        assert(benchmark == 'iperf')
        assert(proxy_info == {})
        assert(benchmark_details == {})
        assert(isinstance(env, func.args_handler.Baremetal))

    def test_cleanup_env(self):
        mock_bm = mock.Mock(spec=func.args_handler.Baremetal)
        func.args_handler.cleanup_env(mock_bm)
        assert mock_bm.cleanup.called

        mock_vm = mock.Mock(spec=func.args_handler.Virtual)
        func.args_handler.cleanup_env(mock_vm)
        assert mock_vm.cleanup.called
