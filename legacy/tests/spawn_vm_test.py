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
from mock import Mock, MagicMock
import os
from qtip.utils.spawn_vm import SpawnVM


class KeystoneMock(MagicMock):
    auth_token = Mock()
    v2_0 = Mock()


class StackMock(MagicMock):
    status = 'COMPLETE'
    outputs = [{'output_key': 'availability_instance_1',
                'output_value': 'output_value_1'},
               {'output_key': 'instance_ip_1',
                "output_value": "172.10.0.154"},
               {"output_key": "instance_PIP_1",
                "output_value": "10.10.17.5"}]


class HeatMock(MagicMock):
    def list(self):
        return []

    def get(self, stackname):
        return StackMock()

    def create(self, stack_name, template):
        pass


class TestClass:
    @pytest.mark.parametrize("test_input, expected", [
        ({'availability_zone': ['compute1', 'compute1'],
          'OS_image': ['QTIP_CentOS', 'QTIP_CentOS'],
          'public_network': ['admin-floating_net', 'admin-floating_net'],
          'flavor': ['m1.large', 'm1.large'],
          'role': ['1-server', '2-host']},
         [('172.10.0.154', '')]),
    ])
    @mock.patch('qtip.utils.spawn_vm.Env_setup')
    @mock.patch('qtip.utils.spawn_vm.AvailabilityZone')
    @mock.patch('qtip.utils.spawn_vm.keystoneclient.v2_0', autospec=True)
    @mock.patch('qtip.utils.spawn_vm.heatclient.client', autospec=True)
    def test_create_zones_success(self, mock_heat, mock_keystone,
                                  mock_zone, mock_setup, test_input, expected):
        open('./config/QtipKey.pub', 'a').close()
        mock_heat.Client.return_value = Mock(stacks=HeatMock())
        k = mock.patch.dict(os.environ, {'INSTALLER_TYPE': 'fuel'})
        k.start()
        SpawnVM(test_input)
        k.stop()
        os.remove('./config/QtipKey.pub')
        mock_setup.ip_pw_list.append.assert_called_with(expected[0])
