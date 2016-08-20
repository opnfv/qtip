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
    @mock.patch('func.args_handler.Env_setup.call_ping_test')
    @mock.patch('func.args_handler.Env_setup.call_ssh_test')
    @mock.patch('func.args_handler.Env_setup.update_ansible')
    @mock.patch('func.args_handler.SpawnVM')
    @mock.patch('func.args_handler.Driver.drive_bench')
    def test_prepare_and_run_benchmark_successful(self, mock_driver, mock_sqawn_vm, mock_env_setup_ping,
                                                  mock_env_setup_ssh, mock_update_ansible, test_input, expected):
        mock_ips = mock.Mock(return_value=["10.20.0.23", "10.20.0.24"])
        func.args_handler.Env_setup.fetch_compute_ips = mock_ips
        func.args_handler.prepare_and_run_benchmark(test_input)
        call = mock_driver.call_args
        call_args, call_kwargs = call
        assert sorted(map(sorted, call_args)) == sorted(map(sorted, expected))
