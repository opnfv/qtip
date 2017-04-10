##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.ansible_library.plugins.action import calculate


@pytest.fixture
def metric_spec():
    return {
        "formual": "geometric mean",
        "name": "ssl_rsa",
        "workloads": {
            "rsa_sign": 500,
            "rsa_verify": 600
        }
    }


@pytest.fixture()
def metrics():
    return {
        "rsa_sign": [500],
        "rsa_verify": [600]
    }


def test_calc_metric_score(metric_spec, metrics):
    expected = {'score': 1.0,
                'spec': {'formual': 'geometric mean',
                         'name': 'ssl_rsa',
                         'workloads': {'rsa_sign': 500, 'rsa_verify': 600}},
                'workload_scores': {'rsa_sign': 1.0,
                                    'rsa_verify': 1.0}}
    assert calculate.calc_metric_score(metric_spec, metrics) == expected
