##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from os import path

import pytest


@pytest.fixture(scope='session')
def data_root():
    return path.join(path.dirname(__file__), 'data')


@pytest.fixture(scope='session')
def resources_root(data_root):
    return path.join(data_root, 'resources')


@pytest.fixture(scope='session')
def metrics():
    return {
        "ssl_rsa": {
            "rsa_sign": [500],
            "rsa_verify": [600]
        }
    }


@pytest.fixture(scope='session')
def metric_spec():
    return {
        "name": "ssl_rsa",
        "workloads": [
            {"name": "rsa_sign"},
            {"name": "rsa_verify"}
        ]
    }


@pytest.fixture(scope='session')
def section_spec(metric_spec):
    return {
        "name": "ssl",
        "description": "cryptography and SSL/TLS performance",
        "metrics": [metric_spec]
    }


@pytest.fixture(scope='session')
def qpi_spec(section_spec):
    return {
        "name": "compute",
        "description": "QTIP Performance Index of compute",
        "sections": [section_spec]
    }


@pytest.fixture(scope='session')
def rsa_sign_baseline():
    return {'name': 'rsa_sign', 'baseline': '500'}


@pytest.fixture(scope='session')
def rsa_verify_baseline():
    return {"name": "rsa_verify", "baseline": 600}


@pytest.fixture(scope='session')
def metric_baseline(rsa_sign_baseline, rsa_verify_baseline):
    return {
        "name": "ssl_rsa",
        "workloads": [rsa_sign_baseline, rsa_verify_baseline]
    }


@pytest.fixture(scope='session')
def section_baseline(metric_baseline):
    return {
        "name": "ssl",
        "metrics": [metric_baseline]
    }


@pytest.fixture(scope='session')
def qpi_baseline(section_baseline):
    return {
        "name": "compute-baseline",
        "description": "The baseline for compute QPI",
        "score": 2048,
        "sections": [section_baseline]
    }


@pytest.fixture(scope='session')
def metric_result():
    return {'score': 1.0,
            'name': 'ssl_rsa',
            'description': 'metric',
            'workloads': [{'description': 'workload', 'name': 'rsa_sign',
                           'score': 1.0, 'result': 500},
                          {'description': 'workload', 'name': 'rsa_verify',
                           'score': 1.0, 'result': 600}]}


@pytest.fixture(scope='session')
def section_result(metric_result):
    return {'score': 1.0,
            'name': 'ssl',
            'description': 'cryptography and SSL/TLS performance',
            'metrics': [metric_result]}


@pytest.fixture(scope='session')
def info():
    return {
        "system_info": {
            "kernel": "4.4.0-72-generic x86_64 (64 bit)",
            "product": "EC600G3",
            "os": "Ubuntu 16.04 xenial",
            "cpu": "2 Deca core Intel Xeon E5-2650 v3s (-HT-MCP-SMP-)",
            "disk": "1200.3GB (25.1% used)",
            "memory": "30769.7/128524.1MB"
        }
    }


@pytest.fixture(scope='session')
def spec():
    """ refers to resources/QPI/compute.yaml """
    return {
        "sections": [{
            "name": "ssl",
            "description": "cryptography and SSL/TLS performance",
            "metrics": [{
                "workloads": [
                    {"name": "rsa_sign",
                     "description": "rsa x bits sign per second"},
                    {"name": "rsa_verify",
                     "description": "rsa x bits verify per second"}]
            }]
        }]
    }


@pytest.fixture(scope='session')
def qpi_result(section_result, info):
    return {'score': 2048,
            'name': 'compute',
            'description': 'QTIP Performance Index of compute',
            'system_info': info,
            'sections': [section_result],
            'spec': "https://git.opnfv.org/qtip/tree/resources/QPI/compute.yaml",
            'baseline': "https://git.opnfv.org/qtip/tree/resources/baselines/compute.json",
            }


@pytest.fixture(scope='session')
def aggregated_report(qpi_result):
    return {
        'score': 2017,
        'name': 'compute',
        'description': 'POD compute QPI',
        'nodes': [qpi_result]
    }
