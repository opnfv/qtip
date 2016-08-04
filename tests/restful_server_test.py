import restful_server.restful_server as server
import pytest
import json


@pytest.fixture
def app():
    return server.app


@pytest.fixture
def app_client(app):
    client = app.test_client()
    return client


class TestClass:
    @pytest.mark.parametrize("body, expected", [
        ({'installer_type': 'fuel',
          'installer_ip': '10.20.0.2'},
         {'job_id': '',
          'installer_type': 'fuel',
          'installer_ip': '10.20.0.2',
          'pod_name': 'default',
          'suit_name': 'all',
          'deadline': 10,
          'type': 'BM',
          'state': 'processing',
          'state_detail': [],
          'result': []}),
        ({'installer_type': 'fuel',
          'installer_ip': '10.20.0.2',
          'pod_name': 'zte-pod1',
          'deadline': 20,
          'suit_name': 'compute',
          'type': 'VM'},
         {'job_id': '',
          'installer_type': 'fuel',
          'installer_ip': '10.20.0.2',
          'pod_name': 'zte-pod1',
          'suit_name': 'compute',
          'deadline': 20,
          'type': 'VM',
          'state': 'processing',
          'state_detail': [],
          'result': []})
    ])
    def test_post_get_delete_job_successful(self, app_client, body, expected):
        reply = app_client.post("/api/v1.0/jobs", data=body)
        print reply.data
        id = json.loads(reply.data)['job_id']
        expected['job_id'] = id
        get_reply = app_client.get("/api/v1.0/jobs/%s" % id)
        reply_data = json.loads(get_reply.data)
        assert len(filter(lambda x: reply_data[x] == expected[x], expected.keys())) == len(expected)
        delete_reply = app_client.delete("/api/v1.0/jobs/%s" % id)
        assert "successful" in delete_reply.data

    @pytest.mark.parametrize("body, expected", [
        ([{'installer_type': 'fuel',
           'installer_ip': '10.20.0.2'},
          {'installer_type': 'compass',
           'installer_ip': '192.168.20.50'}],
         ['job_id',
          'It already has one job running now!']),
        ([{'installer_type': 'fuel',
           'installer_ip': '10.20.0.2'},
          {'installer_type': 'compass',
           'insta_ip': '192.168.20.50'}],
         ['job_id',
          'Installer_ip is required'])
    ])
    def test_post_two_jobs_unsuccessful(self, app_client, body, expected):
        reply_1 = app_client.post("/api/v1.0/jobs", data=body[0])
        reply_2 = app_client.post("/api/v1.0/jobs", data=body[1])
        assert expected[0] in json.loads(reply_1.data).keys()
        app_client.delete("/api/v1.0/jobs/%s" % json.loads(reply_1.data)['job_id'])
        assert expected[1] in json.dumps(reply_2.data)
