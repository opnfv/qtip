##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
import os

from qtip.ansible_library.plugins.action.aggregate import aggregate


def test_aggregate(data_root):
    hosts = ['host1', 'host2']
    pod_results = aggregate(
        hosts=hosts,
        basepath=os.path.join(data_root, 'results'),
        src='qpi.json'
    )
    expected = json.load(open(os.path.join(data_root, 'results', 'expected.json')))
    assert pod_results == expected
