##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import requests

from qtip.reporter.common import validate_params


TEST_API_URL = 'http://testresults.opnfv.org/test/api/v1'


@validate_params()
def push_results(params):
    """ push results to OPNFV TestAPI """

    response = requests.post(TEST_API_URL+'/results',json=params)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        response.raise_for_status()
