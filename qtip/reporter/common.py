##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from qtip.base import error

result_params = {'project_name',
                 'case_name',
                 'pod_name',
                 'installer',
                 'version',
                 'scenario',
                 'criteria',
                 'build_tag',
                 'start_date',
                 'stop_data',
                 'details'}


def validate_params():
    def _decorator(func):
        def _execute(params):
            if set(params.keys()) != result_params:
                missing_parameters = list(result_params - set(params.keys()))
                print "Missing Parameters -- {}". \
                    format(str(missing_parameters))
                raise error.MissingParamsError("push_results",
                                               missing_parameters)
            for key in params.keys():
                if not params[key]:
                    print "Invalid or missing value of parameter `{}`". \
                        format(key)
                    raise error.InvalidParamsError("push_results", key)
            return func(params)

        return _execute
    return _decorator
