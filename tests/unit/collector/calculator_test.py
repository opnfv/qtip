##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.collector.calculator import calculate_compute_benchmark_index


@pytest.mark.parametrize("test_inputs,expected", [
    (['dhrystone',
      {"multi_cpus": {"num": "40", "score": "54038.9"},
       "single_cpu": {"num": "1", "score": "2499.1"},
       "total_cpus": "40"}], 100.28),
    (['whetstone',
      {"multi_cpus": {"num": "40", "score": "19046.9"},
       "single_cpu": {"num": "1", "score": "551.2"},
       "total_cpus": "40"}], 100.13),
    (['dpi', {"bps": 9.278, "pps": 0.989}], 105.49),
    (['ramspeed',
      {"float_add": "9465.59", "float_average": "8301.18",
       "float_copy": "7254.96", "float_scale": "7267.65",
       "float_triad": "9216.53", "integer_add": "10107.75",
       "integer_average": "10118.67", "integer_copy": "10173.10",
       "integer_scale": "10167.38", "integer_triad": "10026.46"}],
     100.37),
    (['ssl',
      {"aes_128_cbc_1024_bytes": "493562.85",
       "aes_128_cbc_16_bytes": "454005.06",
       "aes_128_cbc_256_bytes": "491661.66",
       "aes_128_cbc_64_bytes": "482143.21",
       "aes_128_cbc_8192_bytes": "493306.85",
       "rsa_sign_1024": "5037.7",
       "rsa_sign_2048": "713.6",
       "rsa_sign_4096": "102.1",
       "rsa_sign_512": "14982.3",
       "rsa_verify_1024": "67359.9",
       "rsa_verify_2048": "23458.0",
       "rsa_verify_4096": "6402.9",
       "rsa_verify_512": "180619.2"}], 99.93)
])
def test_calculate_compute_benchmark_index(test_inputs, expected):
    benchmark_index = \
        calculate_compute_benchmark_index(test_inputs[0], test_inputs[1])
    assert benchmark_index == expected
