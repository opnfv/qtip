import pytest
import mock
import os
from func.driver import Driver


class TestClass:
    @pytest.mark.parametrize("test_input, expected", [
        (["iperf",
          [('host', ['10.20.0.13', '10.20.0.15'])],
          "iperf_bm.yaml",
          [('duration', 20), ('protocol', 'tcp'), ('bandwidthGbps', 0)],
          [("10.20.0.13", [None]), ("10.20.0.15", [None])],
          {'http_proxy': 'http://10.20.0.1:8118',
           'https_proxy': 'http://10.20.0.1:8118',
           'no_proxy': 'localhost,127.0.0.1,10.20.*,192.168.*'},
          'fuel'],
         [{'Dest_dir': 'results',
           'ip1': '',
           'ip2': '',
           'installer': 'fuel',
           'workingdir': '/home',
           'fname': 'iperf_bm.yaml',
           'username': 'root',
           'http_proxy': 'http://10.20.0.1:8118',
           'https_proxy': 'http://10.20.0.1:8118',
           'no_proxy': 'localhost,127.0.0.1,10.20.*,192.168.*',
           'duration': 20,
           'protocol': 'tcp',
           'bandwidthGbps': 0,
           "role": "host"}]),
        (["iperf",
          [('1-server', ['10.20.0.13']), ('2-host', ['10.20.0.15'])],
          "iperf_vm.yaml",
          [('duration', 20), ('protocol', 'tcp'), ('bandwidthGbps', 0)],
          [("10.20.0.13", [None]), ("10.20.0.15", [None])],
          {},
          'joid'],
         [{'Dest_dir': 'results',
           'ip1': '10.20.0.13',
           'ip2': '',
           'installer': 'joid',
           "privateip1": "NONE",
           'workingdir': '/home',
           'fname': 'iperf_vm.yaml',
           'username': 'ubuntu',
           'duration': 20,
           'protocol': 'tcp',
           'bandwidthGbps': 0,
           "role": "1-server"},
          {'Dest_dir': 'results',
           'ip1': '',
           'ip2': '',
           'installer': 'joid',
           'workingdir': '/home',
           'fname': 'iperf_vm.yaml',
           'username': 'ubuntu',
           'duration': 20,
           'protocol': 'tcp',
           'bandwidthGbps': 0,
           "role": "2-host"}])
    ])
    @mock.patch('func.driver.AnsibleApi')
    def test_driver_success(self, mock_ansible, test_input, expected):
        mock_ansible.execute_playbook.return_value = True
        k = mock.patch.dict(os.environ, {'INSTALLER_TYPE': test_input[6], 'PWD': '/home'})
        k.start()
        dri = Driver()
        dri.drive_bench(test_input[0], test_input[1], test_input[2], test_input[3], test_input[4], test_input[5])
        call_list = mock_ansible.execute_playbook.call_args_list
        k.stop()
        for call in call_list:
            call_args, call_kwargs = call
            real_call = call_args[3]
            assert real_call == expected[call_list.index(call)]
