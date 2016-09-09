import restful_server.qtip_server as server
import pytest
import json
import mock
import time


@pytest.fixture
def app():
    return server.app


@pytest.fixture
def app_client(app):
    client = app.test_client()
    return client


def side_effect_sleep(sleep_time):
    time.sleep(sleep_time)


def side_effect_pass():
    pass


class TestClass:
    @pytest.mark.parametrize("body, expected", [
        ({'installer_type': 'fuel',
          'installer_ip': '10.20.0.2'},
         {'job_id': '',
          'installer_type': 'fuel',
          'installer_ip': '10.20.0.2',
          'pod_name': 'default',
          'suite_name': 'compute',
          'max-minutes': 60,
          'type': 'BM',
          'state': 'finished',
          'state_detail': [{'state': 'finished', 'benchmark': 'dhrystone_bm.yaml'},
                           {'state': 'finished', 'benchmark': 'whetstone_bm.yaml'},
                           {'state': 'finished', 'benchmark': 'ramspeed_bm.yaml'},
                           {'state': 'finished', 'benchmark': 'dpi_bm.yaml'},
                           {'state': 'finished', 'benchmark': 'ssl_bm.yaml'}],
          'result': []}),
        ({'installer_type': 'fuel',
          'installer_ip': '10.20.0.2',
          'pod_name': 'zte-pod1',
          'max-minutes': 20,
          'suite_name': 'compute',
          'type': 'VM'},
         {'job_id': '',
          'installer_type': 'fuel',
          'installer_ip': '10.20.0.2',
          'pod_name': 'zte-pod1',
          'suite_name': 'compute',
          'max-minutes': 20,
          'type': 'VM',
          'state': 'finished',
          'state_detail': [{u'state': u'finished', u'benchmark': u'dhrystone_vm.yaml'},
                           {u'state': u'finished', u'benchmark': u'whetstone_vm.yaml'},
                           {u'state': u'finished', u'benchmark': u'ramspeed_vm.yaml'},
                           {u'state': u'finished', u'benchmark': u'dpi_vm.yaml'},
                           {u'state': u'finished', u'benchmark': u'ssl_vm.yaml'}],
          'result': []})
    ])
    @mock.patch('restful_server.qtip_server.args_handler.prepare_and_run_benchmark')
    def test_post_get_delete_job_successful(self, mock_args_handler, app_client, body, expected):
        reply = app_client.post("/api/v1.0/jobs", data=body)
        print(reply.data)
        id = json.loads(reply.data)['job_id']
        expected['job_id'] = id
        post_process = ''
        while post_process != 'finished':
            get_reply = app_client.get("/api/v1.0/jobs/%s" % id)
            reply_data = json.loads(get_reply.data)
            post_process = reply_data['state']
            print(reply_data)
        assert len(filter(lambda x: reply_data[x] == expected[x], expected.keys())) == len(expected)
        delete_reply = app_client.delete("/api/v1.0/jobs/%s" % id)
        assert "successful" in delete_reply.data

    @pytest.mark.parametrize("body, expected", [
        ([{'installer_type': 'fuel',
           'installer_ip': '10.20.0.2'},
          {'installer_type': 'compass',
           'installer_ip': '192.168.20.50'}],
         ['job_id',
          'It already has one job running now!'])
    ])
    @mock.patch('restful_server.qtip_server.args_handler.prepare_and_run_benchmark',
                side_effect=[side_effect_sleep(0.5), side_effect_pass])
    def test_post_two_jobs_unsuccessful(self, mock_args_hanler, app_client, body, expected):
        reply_1 = app_client.post("/api/v1.0/jobs", data=body[0])
        reply_2 = app_client.post("/api/v1.0/jobs", data=body[1])
        assert expected[0] in json.loads(reply_1.data).keys()
        app_client.delete("/api/v1.0/jobs/%s" % json.loads(reply_1.data)['job_id'])
        assert expected[1] in json.dumps(reply_2.data)
