##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import requests


TEST_API_URL = 'http://testresults.opnfv.org/test/api/v1'

result_params = {'project_name',
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


def validate_params():
    def _decorator(func):
        def _execute(params):
            if set(params.keys()) != result_params:
                missing_parameters = list(result_params - set(params.keys()))
                print "Missing Parameters -- {}". \
                    format(str(missing_parameters))
                raise MissingParamsError("push_results", missing_parameters)
            for key in params.keys():
                if not params[key]:
                    print "Invalid or missing value of parameter `{}`". \
                        format(key)
                    raise InvalidParamsError("push_results", key)
            return func(params)

        return _execute
    return _decorator


class InvalidParamsError(Exception):
    def __init__(self, method, key):
        self.method = method
        self.key = key


class MissingParamsError(Exception):
    def __init__(self, method, keys):
        self.method = method
        self.key = keys


@validate_params()
def push_results(params):
    """ push results to OPNFV TestAPI """

    response = requests.post(TEST_API_URL + '/results', json=params)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        response.raise_for_status()
