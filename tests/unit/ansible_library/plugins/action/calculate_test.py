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


@pytest.fixture()
def metrics():
    return {
        "ssl_rsa": {
            "rsa_sign": [500],
            "rsa_verify": [600]
        }
    }


@pytest.fixture()
def metric_spec():
    return {
        "name": "ssl_rsa",
        "workloads": [
            {"name": "rsa_sign", "baseline": 500},
            {"name": "rsa_verify", "baseline": 600}
        ]
    }


@pytest.fixture()
def section_spec(metric_spec):
    return {
        "name": "ssl",
        "description": "cryptography and SSL/TLS performance",
        "metrics": [metric_spec]
    }


@pytest.fixture
def qpi_spec(section_spec):
    return {
        "name": "compute",
        "description": "QTIP Performance Index of compute",
        "sections": [section_spec]
    }


@pytest.fixture()
def metric_result():
    return {'score': 1.0,
            'name': 'ssl_rsa',
            'description': 'metric',
            'children': [{'description': 'workload', 'name': 'rsa_sign', 'score': 1.0},
                         {'description': 'workload', 'name': 'rsa_verify', 'score': 1.0}]}


@pytest.fixture()
def section_result(metric_result):
    return {'score': 1.0,
            'name': 'ssl',
            'description': 'cryptography and SSL/TLS performance',
            'children': [metric_result]}


@pytest.fixture()
def qpi_result(section_result, metrics):
    return {'score': 2048,
            'name': 'compute',
            'description': 'QTIP Performance Index of compute',
            'children': [section_result],
            'details': {
                'spec': "https://git.opnfv.org/qtip/tree/resources/QPI/compute.yaml",
                'metrics': metrics}}


def test_calc_metric(metric_spec, metrics, metric_result):
    assert calculate.calc_metric(metric_spec, metrics['ssl_rsa']) == metric_result


def test_calc_section(section_spec, metrics, section_result):
    assert calculate.calc_section(section_spec, metrics) == section_result


def test_calc_qpi(qpi_spec, metrics, qpi_result):
    assert calculate.calc_qpi(qpi_spec, metrics) == qpi_result


@pytest.mark.parametrize('metrics, baseline, expected', [
    (['612376.96k'], '612376.96k', 1)
])
def test_calc_score(metrics, baseline, expected):
    assert calculate.calc_score(metrics, baseline) == expected
