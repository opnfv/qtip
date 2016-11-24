##############################################################################
# Copyright (c) 2016 ZTE and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import pytest
import filecmp
from qtip.utils.env_setup import Env_setup
import mock


DATA_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data')


def get_test_plan(name):
    return os.path.join(DATA_DIR, 'test_plan', name)


def get_output(name):
    return os.path.join(DATA_DIR, 'output', name)


class TestClass:
    @pytest.mark.parametrize("test_input, expected", [
        (get_test_plan("bm_with_proxy.yaml"),
         ["dhrystone",
         {},
         [],
         {'http_proxy': 'http://10.20.0.1:8118',
          'https_proxy': 'http://10.20.0.1:8118',
          'no_proxy': 'localhost,127.0.0.1,10.20.*,192.168.*'}]),
        (get_test_plan("bm_without_proxy.yaml"),
         ["dhrystone",
          {},
          [],
          {}]),
        (get_test_plan("vm.yaml"),
         ["iperf",
          {'availability_zone': ['compute1', 'compute1'],
           'OS_image': ['QTIP_CentOS', 'QTIP_CentOS'],
           'public_network': ['admin-floating_net', 'admin-floating_net'],
           'flavor': ['m1.large', 'm1.large'],
           'role': ['1-server', '2-host']},
          [('duration', 20), ('protocol', 'tcp'), ('bandwidthGbps', 0)],
          {'http_proxy': 'http://10.20.0.1:8118',
           'https_proxy': 'http://10.20.0.1:8118',
           'no_proxy': 'localhost,127.0.0.1,10.20.*,192.168.*'}])])
    def test_parse_success(self, test_input, expected):
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
            test_class.parse(get_test_plan("vm_error.yaml"))
        assert "benchmark" in str(excinfo.value)

    def test_update_ansible(self):
        test_class = Env_setup()
        mock_ips = mock.Mock(return_value=["10.20.0.28", "10.20.0.29"])
        test_class.fetch_compute_ips = mock_ips
        test_class.parse(get_test_plan("bm_without_proxy.yaml"))
        test_class.update_ansible()
        result = filecmp.cmp(get_output("hosts"), "config/hosts")
        assert result

    @pytest.mark.skip(reason="(yujunz) test halt, to be fixed")
    def test_ping(self, capfd):
        test_class = Env_setup()
        mock_ips = mock.Mock(return_value=["127.0.0.1", "10.20.0.29"])
        test_class.fetch_compute_ips = mock_ips
        test_class.parse(get_test_plan("bm_ping.yaml"))
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
