##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import json
import time

import mock
import pytest

import qtip.api.cmd.server as server


def setup_module():
    server.add_routers()


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
          'max_minutes': 60,
          'type': 'BM',
          'testdb_url': None,
          'node_name': None,
          'state': 'finished',
          'state_detail': [{'state': 'finished', 'benchmark': 'dhrystone_bm.yaml'},
                           {'state': 'finished', 'benchmark': 'whetstone_bm.yaml'},
                           {'state': 'finished', 'benchmark': 'ramspeed_bm.yaml'},
                           {'state': 'finished', 'benchmark': 'dpi_bm.yaml'},
                           {'state': 'finished', 'benchmark': 'ssl_bm.yaml'}],
          'result': 0}),
        ({'installer_type': 'fuel',
          'installer_ip': '10.20.0.2',
          'pod_name': 'default',
          'max_minutes': 20,
          'suite_name': 'compute',
          'type': 'VM',
          'benchmark_name': 'dhrystone_vm.yaml',
          'testdb_url': 'http://testresults.opnfv.org/test/api/v1',
          'node_name': 'zte-pod2'},
         {'job_id': '',
          'installer_type': 'fuel',
          'installer_ip': '10.20.0.2',
          'pod_name': 'default',
          'suite_name': 'compute',
          'max_minutes': 20,
          'type': 'VM',
          'testdb_url': 'http://testresults.opnfv.org/test/api/v1',
          'node_name': 'zte-pod2',
          'state': 'finished',
          'state_detail': [{u'state': u'finished', u'benchmark': u'dhrystone_vm.yaml'}],
          'result': 0})
    ])
    @mock.patch('qtip.utils.args_handler.prepare_and_run_benchmark')
    def test_post_get_delete_job_successful(self, mock_args_handler, app_client, body, expected):
        mock_args_handler.return_value = {'result': 0,
                                          'detail': {'host': [(u'10.20.6.14', {'unreachable': 0,
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
                                                                               'failures': 0})]}}

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
    @mock.patch('qtip.utils.args_handler.prepare_and_run_benchmark',
                side_effect=[side_effect_sleep(0.5), side_effect_pass])
    def test_post_two_jobs_unsuccessful(self, mock_args_hanler, app_client, body, expected):
        reply_1 = app_client.post("/api/v1.0/jobs", data=body[0])
        reply_2 = app_client.post("/api/v1.0/jobs", data=body[1])
        assert expected[0] in json.loads(reply_1.data).keys()
        app_client.delete("/api/v1.0/jobs/%s" % json.loads(reply_1.data)['job_id'])
        assert expected[1] in json.dumps(reply_2.data)
