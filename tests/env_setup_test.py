##############################################################################
# Copyright (c) 2016 ZTE and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest
from func.env_setup import Env_setup
import mock
import yaml
import os
import sys


class TestClass:

    @pytest.mark.parametrize("test_input, expected", [
        ("./tests/test_case/bm_with_proxy.yaml", ["dhrystone",
                                                  [],
                                                  {'http_proxy': 'http://10.20.0.1:8118',
                                                   'https_proxy': 'http://10.20.0.1:8118',
                                                   'no_proxy': 'localhost,127.0.0.1,10.20.*,192.168.*'}]),
        ("./tests/test_case/bm_without_proxy.yaml", ["dhrystone",
                                                     [],
                                                     {}]),
        ("./tests/test_case/vm.yaml", ["iperf",
                                       [('duration', 20), ('protocol', 'tcp'), ('bandwidthGbps', 0)],
                                       {'http_proxy': 'http://10.20.0.1:8118',
                                        'https_proxy': 'http://10.20.0.1:8118',
                                        'no_proxy': 'localhost,127.0.0.1,10.20.*,192.168.*'}])
    ])
    def test_handler_args_success(self, test_input, expected):
        f_name = open(test_input)
        doc = yaml.load(f_name)
        f_name.close()
        test_class = Env_setup(doc)
        benchmark, details, proxy = test_class.handler_args()
        assert benchmark == expected[0]
        assert sorted(details) == sorted(expected[1])
        assert proxy == expected[2]

    def test_handler_args_failed(self):
        test_case = "./tests/test_case/error.yaml"
        f_name = open(test_case)
        doc = yaml.load(f_name)
        f_name.close()
        test_class = Env_setup(doc)
        with pytest.raises(KeyError) as excinfo:
            test_class.handler_args()
        assert "benchmark" in str(excinfo.value)

