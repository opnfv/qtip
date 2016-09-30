import pytest
import mock
from func.driver import Driver


class TestClass:
    @pytest.mark.parametrize("test_input, expected", [
        (['fuel',
          '/home',
          "iperf",
          [('host', ['10.20.0.13', '10.20.0.15'])],
          "iperf_bm.yaml",
          [('duration', 20), ('protocol', 'tcp'), ('bandwidthGbps', 0)],
          [("10.20.0.13", [None]), ("10.20.0.15", [None])],
          {'http_proxy': 'http://10.20.0.1:8118',
           'https_proxy': 'http://10.20.0.1:8118',
           'no_proxy': 'localhost,127.0.0.1,10.20.*,192.168.*'}],
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
        (['joid',
          '/home',
          "iperf",
          [('1-server', ['10.20.0.13']), ('2-host', ['10.20.0.15'])],
          "iperf_vm.yaml",
          [('duration', 20), ('protocol', 'tcp'), ('bandwidthGbps', 0)],
          [('1-server', '10.10.17.4'), ('2-host', '10.10.17.5')],
          {}],
         [{'Dest_dir': 'results',
           'ip1': '10.20.0.13',
           'ip2': '',
           'installer': 'joid',
           'privateip1': '10.10.17.4',
           'workingdir': '/home',
           'fname': 'iperf_vm.yaml',
           'username': 'ubuntu',
           'duration': 20,
           'protocol': 'tcp',
           'bandwidthGbps': 0,
           "role": "1-server"},
          {'Dest_dir': 'results',
           'ip1': '10.20.0.13',
           'ip2': '',
           'installer': 'joid',
           'privateip1': '10.10.17.4',
           'workingdir': '/home',
           'fname': 'iperf_vm.yaml',
           'username': 'ubuntu',
           'duration': 20,
           'protocol': 'tcp',
           'bandwidthGbps': 0,
           "role": "2-host"}])
    ])
    @mock.patch('func.driver.AnsibleApi.execute_playbook')
    @mock.patch('func.driver.AnsibleApi.get_detail_playbook_stats')
    def test_driver_success(self, mock_stats, mock_ansible, test_input, expected):
        mock_ansible.return_value = True
        mock_stats.return_value = [(u'10.20.6.14', {'unreachable': 0,
                                                    'skipped': 13,
                                                    'ok': 27,
                                                    'changed': 26,
                                                    'failures': 0}),
                                   ('localhost', {'unreachable': 0,
                                                  'skipped': 0,
                                                  'ok': 6,
                                                  'changed': 6,
                                                  'failures': 0}),
                                   (u'10.20.6.13', {'unreachable': 0,
                                                    'skipped': 13,
                                                    'ok': 27,
                                                    'changed': 26,
                                                    'failures': 0})]
        dri = Driver()
        result = dri.drive_bench(test_input[0], test_input[1], test_input[2], test_input[3],
                                 test_input[4], test_input[5], test_input[6], test_input[7])
        call_list = mock_ansible.call_args_list
        for call in call_list:
            call_args, call_kwargs = call
            real_call = call_args[3]
            assert real_call == expected[call_list.index(call)]
        assert result['result'] == 0
