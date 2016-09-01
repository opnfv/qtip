import pytest
import mock
from mock import Mock, MagicMock
import os
from func.virtual_setup import Virtual


class KeystoneMock(MagicMock):
    auth_token = Mock()
    v2_0 = Mock()


class ImageMock(MagicMock):
    name = 'QTIP_CentOS'


class ImagesMock(MagicMock):
    def list(self):
        return [ImageMock()]


class StackMock(MagicMock):
    status = 'COMPLETE'
    outputs = [{'output_key': 'availability_instance_1',
                'output_value': 'output_value_1'},
               {'output_key': 'instance_PIP_1',
                "output_value": "172.10.0.154"},
               {"output_key": "instance_FIP_1",
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
    @mock.patch('func.virtual_setup.Env_setup')
    @mock.patch('func.virtual_setup.FetchImg')
    @mock.patch('func.virtual_setup.AvailabilityZone')
    @mock.patch('func.virtual_setup.glanceclient', autospec=True)
    @mock.patch('func.virtual_setup.keystoneclient.v2_0', autospec=True)
    @mock.patch('func.virtual_setup.heatclient.client', autospec=True)
    def test_create_zones_success(self, mock_heat, mock_keystone, mock_glance,
                                  mock_zone, mock_fetch,
                                  mock_setup, test_input, expected):
        mock_glance.Client.return_value = Mock(images=ImagesMock())
        #mock_nova_client.Client.return_value = Mock()
        mock_heat.Client.return_value = Mock(stacks=HeatMock())
        k = mock.patch.dict(os.environ, {'INSTALLER_TYPE': 'fuel'})
        k.start()
        Virtual(test_input)
        k.stop()
        mock_setup.ip_pw_list.append.assert_called
