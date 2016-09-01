##############################################################################
# Copyright (c) 2016 ZTE and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest
import filecmp
from func.baremetal_setup import Baremetal
import mock
from mock import MagicMock
import yaml


class TestClass:

    @mock.patch("func.env_setup.Env_setup")
    @mock.patch("func.baremetal_setup.Baremetal.get_host_machine_info")
    def test_init(self, mock_parent_init, mock_get_host_machine_info):
        Baremetal()
        mock_parent_init.assert_called
        mock_get_host_machine_info.assert_called

    def test_check_machine_ips_without_ip(self):
        test_class = Baremetal()
        mock_ips = mock.Mock(return_value=["10.20.0.28", "10.20.0.29"])
        test_class.fetch_compute_ips = mock_ips
        inputs = {"machine_1": {"ip": "", "pw": "", "role": "host"},
                  "machine_2": {"ip": "", "pw": "", "role": "host"}}
        test_class.check_machine_ips(inputs)
        assert inputs["machine_1"]['ip'] in ["10.20.0.28", "10.20.0.29"]
        assert inputs["machine_2"]['ip'] in ["10.20.0.28", "10.20.0.29"]
        assert inputs["machine_1"]['ip'] != inputs["machine_2"]['ip']

    def test_check_machine_ips_with_ip(self):
        test_class = Baremetal()
        mock_ips = mock.Mock(return_value=["10.20.0.28", "10.20.0.29"])
        test_class.fetch_compute_ips = mock_ips
        inputs = {"machine_1": {"ip": "10.20.0.28", "pw": "", "role": "host"},
                  "machine_2": {"ip": "10.20.0.29", "pw": "", "role": "host"}}
        test_class.check_machine_ips(inputs)
        assert inputs["machine_1"]['ip'] in ["10.20.0.28", "10.20.0.29"]
        assert inputs["machine_2"]['ip'] in ["10.20.0.28", "10.20.0.29"]
        assert inputs["machine_1"]['ip'] != inputs["machine_2"]['ip']

    def test_check_machine_ips_with_invalid_ip(self):
        test_class = Baremetal()
        mock_ips = mock.Mock(return_value=["10.20.0.28", "10.20.0.29"])
        test_class.fetch_compute_ips = mock_ips
        inputs = {"machine_1": {"ip": "10.20.0.3", "pw": "", "role": "host"},
                  "machine_2": {"ip": "10.20.0.4", "pw": "", "role": "host"}}
        with pytest.raises(RuntimeError):
            test_class.check_machine_ips(inputs)
