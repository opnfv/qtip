import pytest
import filecmp
from func.env_setup import Env_setup
import mock


class TestClass:

    @pytest.mark.parametrize("test_input, expected", [
        ("tests/test_case/bm_with_proxy.yaml", ["dhrystone",
                                                {},
                                                [],
                                                {'http_proxy': 'http://10.20.0.1:8118',
                                                 'https_proxy': 'http://10.20.0.1:8118',
                                                 'no_proxy': 'localhost,127.0.0.1,10.20.*,192.168.*'}]),
        ("tests/test_case/bm_without_proxy.yaml", ["dhrystone",
                                                   {},
                                                   [],
                                                   {}]),
        ("tests/test_case/vm.yaml", ["iperf",
                                     {'availability_zone': ['compute1', 'compute1'],
                                      'OS_image': ['QTIP_CentOS', 'QTIP_CentOS'],
                                      'public_network': ['admin-floating_net', 'admin-floating_net'],
                                      'flavor': ['m1.large', 'm1.large'],
                                      'role': ['1-server', '2-host']},
                                     [('duration', 20), ('protocol', 'tcp'), ('bandwidthGbps', 0)],
                                     {'http_proxy': 'http://10.20.0.1:8118',
                                      'https_proxy': 'http://10.20.0.1:8118',
                                      'no_proxy': 'localhost,127.0.0.1,10.20.*,192.168.*'}])
    ])
    def test_parse_success(self, test_input, expected):
        print (test_input)
        print (expected)
        test_class = Env_setup()
        mock_ips = mock.Mock(return_value=["10.20.0.28", "10.20.0.29"])
        test_class.fetch_compute_ips = mock_ips
        benchmark, vm_para, details, proxy = \
            test_class.parse(test_input)
        assert benchmark == expected[0]
        assert vm_para == expected[1]
        assert sorted(details) == sorted(expected[2])
        assert proxy == expected[3]

    def test_parse_vm_error(self):
        test_class = Env_setup()
        mock_ips = mock.Mock(return_value=["10.20.0.28", "10.20.0.29"])
        test_class.fetch_compute_ips = mock_ips
        with pytest.raises(KeyError) as excinfo:
            test_class.parse("tests/test_case/vm_error.yaml")
        assert "benchmark" in str(excinfo.value)

    def test_update_ansible(self):
        test_class = Env_setup()
        mock_ips = mock.Mock(return_value=["10.20.0.28", "10.20.0.29"])
        test_class.fetch_compute_ips = mock_ips
        test_class.parse("tests/test_case/bm_without_proxy.yaml")
        test_class.update_ansible()
        result = filecmp.cmp('tests/output/hosts', 'data/hosts')
        assert result

    def test_ping(self, capfd):
        test_class = Env_setup()
        mock_ips = mock.Mock(return_value=["127.0.0.1", "10.20.0.29"])
        test_class.fetch_compute_ips = mock_ips
        test_class.parse("tests/test_case/bm_ping.yaml")
        test_class.call_ping_test()
        resout, reserr = capfd.readouterr()
        assert '127.0.0.1 is UP' in resout

    def test_check_machine_ips_without_ip(self):
        test_class = Env_setup()
        mock_ips = mock.Mock(return_value=["10.20.0.28", "10.20.0.29"])
        test_class.fetch_compute_ips = mock_ips
        inputs = {"machine_1": {"ip": "", "pw": "", "role": "host"},
                  "machine_2": {"ip": "", "pw": "", "role": "host"}}
        test_class.check_machine_ips(inputs)
        assert inputs["machine_1"]['ip'] in ["10.20.0.28", "10.20.0.29"]
        assert inputs["machine_2"]['ip'] in ["10.20.0.28", "10.20.0.29"]
        assert inputs["machine_1"]['ip'] != inputs["machine_2"]['ip']

    def test_check_machine_ips_with_ip(self):
        test_class = Env_setup()
        mock_ips = mock.Mock(return_value=["10.20.0.28", "10.20.0.29"])
        test_class.fetch_compute_ips = mock_ips
        inputs = {"machine_1": {"ip": "10.20.0.28", "pw": "", "role": "host"},
                  "machine_2": {"ip": "10.20.0.29", "pw": "", "role": "host"}}
        test_class.check_machine_ips(inputs)
        assert inputs["machine_1"]['ip'] in ["10.20.0.28", "10.20.0.29"]
        assert inputs["machine_2"]['ip'] in ["10.20.0.28", "10.20.0.29"]
        assert inputs["machine_1"]['ip'] != inputs["machine_2"]['ip']

    def test_check_machine_ips_with_invalid_ip(self):
        test_class = Env_setup()
        mock_ips = mock.Mock(return_value=["10.20.0.28", "10.20.0.29"])
        test_class.fetch_compute_ips = mock_ips
        inputs = {"machine_1": {"ip": "10.20.0.3", "pw": "", "role": "host"},
                  "machine_2": {"ip": "10.20.0.4", "pw": "", "role": "host"}}
        with pytest.raises(RuntimeError):
            test_class.check_machine_ips(inputs)
