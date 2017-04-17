##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

# OPNFV Testapi Client
#
# API url: http://testresults.opnfv.org/test/api/v1
# API spec:
# - http://testresults.opnfv.org/test/swagger/spec.html#!/spec/queryTestResults
# - http://testresults.opnfv.org/test/swagger/spec.html#!/spec/createTestResult
# Login:
#   username: opnfv
#   password: contact admin
# Self host: https://github.com/opnfv/releng/tree/master/utils/test/testapi/deployment

import requests

payload_template = {'project_name',
                    'case_name',
                    'pod_name',
                    'installer',
                    'version',
                    'scenario',
                    'criteria',
                    'build_tag',
                    'start_date',
                    'stop_date',
                    'details'}


def validate_payload():
    def _decorator(func):
        def _execute(testapi_url, payload):
            if set(payload.keys()) != payload_template:
                missing_parameters = list(payload_template -
                                          set(payload.keys()))
                print("Missing Parameters -- {}".
                      format(",".join(missing_parameters)))
                raise MissingParamsError("push_results", missing_parameters)
            invalid_params = []
            for key in payload:
                if (payload[key] == "") or (payload[key] is None):
                    invalid_params.append(key)
            if len(invalid_params) > 0:
                print ("Invalid or missing values of parameters -- `{}`".
                       format(",".join(invalid_params)))
                raise InvalidParamsError("push_results", invalid_params)
            return func(testapi_url, payload)

        return _execute

    return _decorator


class InvalidParamsError(Exception):
    def __init__(self, method, params):
        self.method = method
        self.params = params


class MissingParamsError(Exception):
    def __init__(self, method, params):
        self.method = method
        self.params = params


@validate_payload()
def push_results(testapi_url, payload):
    """ push results to OPNFV TestAPI """

    response = requests.post(testapi_url + '/results', json=payload)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        response.raise_for_status()
