import pytest
import mock
from mock import Mock, MagicMock
import os
from func.spawn_vm import SpawnVM


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
                "output_value": "10.10.17.5"},
               {'output_key': 'KeyPair_PublicKey',
                "output_value": "-----BEGIN RSA PRIVATE KEY-----\nMIIEpwIBAAKCAQEAqCiHcrLBXtxG0LhnKndU7VIVpYxORmv0d4tvujkWOkYuagiW\nU/MTRk0zhRvFQDVPEs0Jrj/BIecqm6fjjT6dZ/H7JLYGaqJitRkoupKgBsMSIqUz\nrR0ekOlfXZ6N+Ud8k6s+qjc7BO4b1ezz78jHisC5o0GCkUV0ECx64Re1fO+oKs1c\nfL9aaexahJUYN3J48pazQz+imc2x/G9nuqHX3cqEszmxnT4jwv//In1GjHy2AyXw\n1oA5F6wZoQCSrXc2BditU+1tlVhEkPFt5JgiHUpY8T8mYbroT7JH6xjcGSKUN+HG\nN8PXNUTD1VAQfwHpkfsGMfDyzjytCXsoTEOqnwIDAQABAoIBAAEL/4vfQQTuKiKy\ngzHofEbd8/SL4xDdKzBzVca7BEBon3FZjFYJdV1CrcduXNQBgPSFAkJrczBa2BEQ\nAoKmmSREhWO9Hl0blbG67l36+7QPEtXUYXX6cG5Ghal3izq6DzR8JG+62Es3kETM\nrNgZT+S1PnKdvcpZvFc9b6ZnF2InuTbrmNVBZKrhdWOJ5tCwRGKKUl6BHoJH3yu0\nT5hUW277e1LYHx+hZtoZ98ToC+LGe6/M8a8y6VLYpcQlX2AtVXeGDalomunF+p3f\nuY6din6s4lq1gSJz03PTpUbwiuhYCTe8Xkseu74Y+XYYJXPHopFju0Ewd6p0Db9Q\nJzzxCoECggCBAM2ox9zyrDc/Vlc0bb9SciFGUd/nEJF89+UHy98bAkpo22zNZIDg\nfacSgkg/6faZD+KrOU0I5W7m2B5t6w2fNHHik6NYGSLQ1JhgbXELGV7X/qECDL02\nctPaf+8o+dYoZja2LdJNASq2nmEmPI3LSHhzAt4dWY4W+geXiHt4iWVHAoIAgQDR\nUdN09xv4U+stWqNcSfgjtx6boEUE8Ky7pyj+LrZKG0L61Jy9cSDP0x0rCtkW9vVR\n6RjidWM/DHQ5cl6aq+7pPy20/OqtqttFYT4R+C3AoAnRSaNzPD9a80C2gjv7WEz0\nPPFstWkI1gsN71KKRx7e6NIa9CNn5x9iE+SGfjgb6QKCAIBXylzG7LCnRNpOj4rp\nyP//RE1fDvv7nyUTF6jnrFfl+6zvXR4yBaKd10DWJrJxGhW15PGo+Ms39EL9el6E\nihmRI+9yIwFX411dToxpXRuPaRTBFmbpvnx2Ayfpp8w+pzA62rnktApzeVFSl0fy\nH3zoLfBjcJPyG8zPwNf6HRJJsQKCAIAE2S5asTaWo+r4m/bYtmXm/eDZnfa7TI/T\nsOWELbTPNp5wjOgsgyhNaAhu7MtmesXn5cxLwohP94vhoMKMNptMD8iRPqJ471Iw\n4zW62NLGeW6AyIHes3CMPMIs+AtHoR33MkotSG5sY/jRk8+HoGoYo6/qK+l+CJ5z\neR579wR5sQKCAIAvPWq+bvcPTDKUU1Fe/Y/GyWoUA+uSqmCdORBkK38lALFGphxj\nfDz9dXskimqW+A9hOPOS8dm8YcVvi/TLXVE5Vsx9VkOg6z6AZBQpgNXGfOgpju4W\nbjER7bQaASatuWQyCxbA9oNlAUdSeOhGTxeFLkLj7hNMd6tLjfd8w7A/hA==\n-----END RSA PRIVATE KEY-----\n"}]


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
    @mock.patch('func.spawn_vm.Env_setup')
    @mock.patch('func.spawn_vm.FetchImg')
    @mock.patch('func.spawn_vm.create_zones')
    @mock.patch('func.spawn_vm.client', autospec=True)
    @mock.patch('func.spawn_vm.keystoneclient.v2_0', autospec=True)
    @mock.patch('func.spawn_vm.heatclient.client', autospec=True)
    def test_create_zones_success(self, mock_heat, mock_keystone,
                                  mock_nova_client, mock_zone, mock_fetch,
                                  mock_setup, test_input, expected):
        mock_nova_client.Client.return_value = Mock()
        mock_heat.Client.return_value = Mock(stacks=HeatMock())
        k = mock.patch.dict(os.environ, {'INSTALLER_TYPE': 'fuel'})
        k.start()
        SpawnVM(test_input)
        k.stop()
        mock_setup.ip_pw_list.append.assert_called_with(expected[0])
