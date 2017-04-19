##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import mock
import pytest

from qtip.reporter import testapi


@pytest.mark.parametrize("testapi_url, payload", [
    ("http://testresults.opnfv.org/test/api/v1", {'project_name': 'qtip',
                                                  'case_name': 'fake-case',
                                                  'pod_name': 'fake_pod',
                                                  'installer': 'fake_installer',
                                                  'version': '1',
                                                  'scenario': 'fake_scenario',
                                                  'criteria': 'fake_criteria',
                                                  'build_tag': 'fake_tag',
                                                  'start_date': 'fake_date',
                                                  'stop_date': 'fake_date',
                                                  'details': 'fake:details'}),
])
@mock.patch('qtip.reporter.testapi.requests')
def test_testapi_unavailable(mock_request, testapi_url, payload):
    mock_request.post.return_value.status_code = testapi.requests.codes.unavailable
    mock_request.post.return_value.reason = 'Service unavailable'
    testapi.push_results(testapi_url, payload)
    mock_request.post.assert_called_with(testapi_url + '/results', json=payload)
    mock_request.post.return_value.raise_for_status.assert_called()


@pytest.mark.parametrize("testapi_url, payload", [
    ("http://testresults.opnfv.org/test/api/v1", {'project_name': 'qtip',
                                                  'case_name': 'fake-case',
                                                  'pod_name': 'fake_pod',
                                                  'installer': 'fake_installer',
                                                  'version': '1',
                                                  'scenario': 'fake_scenario',
                                                  'criteria': 'fake_criteria',
                                                  'build_tag': 'fake_tag',
                                                  'start_date': 'fake_date',
                                                  'stop_date': 'fake_date',
                                                  'details': 'fake:details'}),
])
@mock.patch('qtip.reporter.testapi.requests')
def test_push_results_success(mock_request, testapi_url, payload):
    mock_request.post.return_value.status_code = testapi.requests.codes.ok
    mock_request.post.return_value.json.return_value = {'href': 'mock_url'}
    push_response = testapi.push_results(testapi_url, payload)
    mock_request.post.assert_called_with(testapi_url + '/results', json=payload)
    assert push_response['href'] == 'mock_url'


@pytest.mark.parametrize("testapi_url, payload", [
    ("http://testresults.opnfv.org/test/api/v1", {'project_name': 'qtip',
                                                  'case_name': 'fake-case',
                                                  'pod_name': 'fake_pod',
                                                  'installer': 'fake_installer',
                                                  'version': '1',
                                                  'scenario': 'fake_scenario',
                                                  'criteria': 'fake_criteria',
                                                  'build_tag': 'fake_tag',
                                                  'start_date': 'fake_date',
                                                  'stop_date': 'fake_date',
                                                  'details': 'fake:details'}),
])
@mock.patch('qtip.reporter.testapi.requests')
def test_push_results_not_found(mock_request, testapi_url, payload):
    mock_request.post.return_value.status_code = testapi.requests.codes.not_found
    mock_request.post.return_value.reason = 'Not found'
    testapi.push_results(testapi_url, payload)
    mock_request.post.assert_called_with(testapi_url + '/results', json=payload)
    mock_request.post.return_value.raise_for_status.assert_called()


@pytest.mark.parametrize("testapi_url, payload", [
    ("http://testresults.opnfv.org/test/api/v1", {'project_name': 'qtip',
                                                  'case_name': 'fake-case',
                                                  'pod_name': 'fake_pod',
                                                  'installer': 'fake_installer',
                                                  'version': '',
                                                  'scenario': None,
                                                  'criteria': 'fake_criteria',
                                                  'build_tag': 'fake_tag',
                                                  'start_date': 'fake_date',
                                                  'stop_date': 'fake_date',
                                                  'details': 'fake:details'}),
])
def test_push_results_invalid_params(testapi_url, payload):
    with pytest.raises(testapi.InvalidParamsError) as error_invalid:
        testapi.push_results(testapi_url, payload)
    assert set(error_invalid.value.params) == {'version', 'scenario'}


@pytest.mark.parametrize("testapi_url, payload", [
    ("http://testresults.opnfv.org/test/api/v1", {'project_name': 'qtip',
                                                  'case_name': 'fake-case',
                                                  'pod_name': 'fake_pod',
                                                  'installer': 'fake_installer',
                                                  'criteria': 'fake_criteria',
                                                  'build_tag': 'fake_tag',
                                                  'start_date': 'fake_date',
                                                  'stop_date': 'fake_date',
                                                  'details': 'fake:details'}),
])
def test_push_results_missing_params(testapi_url, payload):
    with pytest.raises(testapi.MissingParamsError) as error_missing:
        testapi.push_results(testapi_url, payload)
    assert set(error_missing.value.params) == {'version', 'scenario'}
