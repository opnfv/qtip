import pytest
import mock
from mock import Mock, MagicMock
import os
from func.create_zones import create_zones

return_list = []


def get_agg_mock(host):
    agg = Mock()
    agg.name = host
    agg.id = host
    return agg


class HyperMock(MagicMock):
    def list(self):
        mock_hypervisor = [Mock(service={'host': '10.20.0.4'}), Mock(service={'host': '10.20.0.5'})]
        return mock_hypervisor


class AggMock(MagicMock):
    def get_details(self, agg_id):
        print "get_detail:{0}".format(agg_id)
        return Mock(hosts=[])

    def create(self, host, agg):
        print "create:{0}:{1}".format(host, agg)
        return agg

    def list(self):
        return return_list

    def delete(self, agg_id):
        print "delete:{0}".format(agg_id)
        pass

    def add_host(self, aggregate, host):
        print "add_host:{0}:{1}".format(aggregate, host)
        pass

    def remove_host(self, agg_id, host):
        pass


class NovaMock(MagicMock):
    hypervisors = HyperMock()
    aggregates = AggMock()


class TestClass:
    @pytest.mark.parametrize("test_input, expected", [
        ([[], ['compute1', 'compute2']],
         ['create:10.20.0.4:compute1',
          'add_host:compute1:10.20.0.4',
          'create:10.20.0.5:compute2',
          'add_host:compute2:10.20.0.5']),
        ([[get_agg_mock('10.20.0.4'), get_agg_mock('10.20.0.5')], ['compute1', 'compute2']],
         ['delete:10.20.0.4',
          'create:10.20.0.4:compute1',
          'get_detail:10.20.0.4',
          'add_host:10.20.0.4:10.20.0.4',
          'delete:10.20.0.5',
          'create:10.20.0.5:compute2',
          'get_detail:10.20.0.5',
          'add_host:10.20.0.5:10.20.0.5']),
        ([[], ['compute1', 'compute5']],
         ['The specified compute node doesnt exist. using compute 1'])
    ])
    @mock.patch('func.create_zones.client', autospec=True)
    @mock.patch('func.create_zones.v2', autospec=True)
    @mock.patch('func.create_zones.session')
    def test_create_zones_success(self, mock_keystone_session, mock_keystone_v2, mock_nova_client, test_input, expected, capfd):
        global return_list
        return_list = test_input[0]
        nova_obj = NovaMock()
        mock_nova_client.Client.return_value = nova_obj()
        k = mock.patch.dict(os.environ, {'OS_AUTH_URL': 'http://172.10.0.5:5000',
                                         'OS_USERNAME': 'admin',
                                         'OS_PASSWORD': 'admin',
                                         'OS_TENANT_NAME': 'admin'})
        k.start()
        create = create_zones()
        create.create_agg(test_input[1])
        k.stop()
        resout, reserr = capfd.readouterr()
        for x in expected:
            assert x in resout
